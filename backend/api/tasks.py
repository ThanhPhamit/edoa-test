import json

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, F, OuterRef, Subquery
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from urllib.parse import urlparse

import datetime
import time
import re
import openai
import logging

from .models import (
    JobCategory,
    JobseekerHistoryNotification,
    Jobseeker,
    Record,
    OrganizationCompany,
    JobLoading,
)
from .jobloading.fetcher import fetch_from_url
from .jobloading.result import JobLoadingResult

logger = logging.getLogger(__name__)


@shared_task
def periodic_exec_mail_agent_intention():
    # 直近n時間以内かつ未送信の通知を取り出す
    notification_all = JobseekerHistoryNotification.objects.filter(
        is_send=False, created_at__gt=timezone.now() - datetime.timedelta(hours=6)
    )

    # 応募意向の通知を抽出する
    notification_intention = notification_all.exclude(record__is_long_time=True)
    notification_intention = notification_intention.filter(
        Q(record__trigger="apply") | Q(record__trigger="cancel_apply")
    )

    # 送信対象の求職者を抽出する
    jobseeker_ids_intention = notification_intention.distinct().values_list(
        "record__proposal__jobseeker__id", flat=True
    )
    jobseekers_intention = Jobseeker.objects.filter(id__in=jobseeker_ids_intention)

    for jobseeker_intention in jobseekers_intention:
        with transaction.atomic():
            # 本番環境以外では社内ドメイン以外にメール送付しない
            if settings.IS_EMAIL_LIMIT is True and jobseeker_intention.in_charge:
                if jobseeker_intention.in_charge.email:
                    if not jobseeker_intention.in_charge.email.endswith(
                        "@props-inc.com"
                    ):
                        continue

            notification_intention_jobseeker = notification_intention.filter(
                record__proposal__jobseeker__id=jobseeker_intention.id
            )

            # 直近n分のアクションがある求職者の応募意向通知はしない
            if (
                notification_intention_jobseeker.filter(
                    created_at__gt=timezone.now() - datetime.timedelta(minutes=15)
                ).count()
                > 0
            ):
                continue

            # 提案ごとに最新の応募意向のみを通知する
            latest_notification = notification_intention_jobseeker.filter(
                record__proposal__id=OuterRef("record__proposal__id")
            ).order_by("-created_at")
            latest_notification_intention_jobseeker = (
                notification_intention_jobseeker.annotate(
                    latest_notification=Subquery(
                        latest_notification.values("created_at")[:1]
                    )
                ).filter(latest_notification=F("created_at"))
            )

            # メールを作成する
            context = {
                "jobseeker": {
                    "id": jobseeker_intention.id,
                    "name": jobseeker_intention.name,
                },
                "jobs": {
                    "apply": [
                        {
                            "company": notification.record.proposal.job.organization_company.name,
                            "position": notification.record.proposal.job.position,
                        }
                        for notification in latest_notification_intention_jobseeker
                        if notification.record.trigger == "apply"
                    ],
                    "cancel_apply": [
                        {
                            "company": notification.record.proposal.job.organization_company.name,
                            "position": notification.record.proposal.job.position,
                        }
                        for notification in latest_notification_intention_jobseeker
                        if notification.record.trigger == "cancel_apply"
                    ],
                },
            }
            mail_intention_html = render_to_string(
                "mailers/notification_intention.html", context
            )
            mail_intention_txt = strip_tags(mail_intention_html)

            # メールを送信する
            for _ in range(5):
                is_success = send_mail(
                    subject=f"{jobseeker_intention.name}さまより応募意向が届きました",
                    message=mail_intention_txt,
                    from_email="リクミイ <no-reply@props-inc.com>",
                    recipient_list=[jobseeker_intention.in_charge.email],
                    html_message=mail_intention_html,
                )
                if is_success == 1:
                    break
                else:
                    time.sleep(1)

            # 送信済にする
            if is_success == 1:
                for notification in notification_intention_jobseeker:
                    instance = JobseekerHistoryNotification.objects.get(
                        id=notification.id
                    )
                    instance.is_send = True
                    instance.save()


@shared_task
def exec_mail_agent_longtime(id):
    record = Record.objects.get(id=id)
    # 本番環境以外では社内ドメイン以外にメール送付しない
    if settings.IS_EMAIL_LIMIT is True and record.proposal.jobseeker.in_charge:
        if record.proposal.jobseeker.in_charge.email:
            if not record.proposal.jobseeker.in_charge.email.endswith("@props-inc.com"):
                return False
    # メールを作成する
    context = {
        "jobseeker": {
            "id": record.proposal.jobseeker.id,
            "name": record.proposal.jobseeker.name,
            "before_record_at": record.before_record_at.date().strftime("%Y.%m.%d"),
        },
    }
    mail_longtime_html = render_to_string("mailers/notification_longtime.html", context)
    mail_longtime_txt = strip_tags(mail_longtime_html)

    # メールを送信する
    for _ in range(5):
        is_success = send_mail(
            subject=f"{record.proposal.jobseeker.name}さまが久々に求人にアクセスしました",
            message=mail_longtime_txt,
            from_email="リクミイ <no-reply@props-inc.com>",
            recipient_list=[record.proposal.jobseeker.in_charge.email],
            html_message=mail_longtime_html,
        )
        if is_success == 1:
            break
        else:
            time.sleep(1)


@shared_task
def exec_mail_ops_add_company(id):
    # 本番環境以外ではメール送付しない
    if settings.IS_EMAIL_LIMIT is True:
        return False

    organization_company = OrganizationCompany.objects.get(id=id)

    # メールを作成する
    context = {
        "company": {
            "id": organization_company.id,
            "name": organization_company.name,
            "company_url": organization_company.company_url,
        },
        "organization": {"name": organization_company.organization.name},
    }
    mail_add_company_html = render_to_string(
        "mailers/notification_add_company.html", context
    )
    mail_add_company_txt = strip_tags(mail_add_company_html)

    # メールを送信する
    for _ in range(5):
        is_success = send_mail(
            subject=f"{organization_company.organization.name}が企業を追加しました",
            message=mail_add_company_txt,
            from_email="リクミイ <no-reply@props-inc.com>",
            recipient_list=[],  # 自社のメールアドレスを入力してください
            html_message=mail_add_company_html,
        )
        if is_success == 1:
            break
        else:
            time.sleep(1)


@shared_task
def exec_mail_jobseeker_proposal(id):
    jobseeker = Jobseeker.objects.get(id=id)
    # 本番環境以外では社内ドメイン以外にメール送付しない
    if settings.IS_EMAIL_LIMIT is True and jobseeker.email:
        if not jobseeker.email.endswith("@props-inc.com"):
            return False

    # メールを作成する
    context = {
        "jobseeker": {
            "id": jobseeker.id,
            "name": jobseeker.name,
        },
        "in_charge": {
            "name": jobseeker.in_charge.name,
            "organization": jobseeker.in_charge.organization.name,
            "email": jobseeker.in_charge.email,
        },
    }
    mail_html = render_to_string(
        "mailers/notification_jobseeker_proposal.html", context
    )
    mail_txt = strip_tags(mail_html)

    # メールを送信する
    for _ in range(5):
        is_success = send_mail(
            subject=f"{jobseeker.in_charge.organization.name}の{jobseeker.in_charge.name}からおすすめの求人の提案がありました。",
            message=mail_txt,
            from_email="リクミイ <no-reply@props-inc.com>",
            recipient_list=[jobseeker.email],
            html_message=mail_html,
        )
        if is_success == 1:
            break
        else:
            time.sleep(1)


# NOTE: プロンプト内では、Outputの順番は極めて重要. 先に生成された情報を踏まえて後の情報が生成されるため.
def constructPrompt(jobPosting, job_category_names):
    return (
        "### Order\n"
        "You are a professional recruiter. Given Japanese job postings, please organize the information in a way that is easy for job seekers to understand and generate a Japanese JSON that meets the following output conditions.\n"
        "To make the text easy to read, the content of the text fields should be formated using new line characters and indents.\n"
        "### Job posting\n"
        f"{jobPosting}\n"
        "### Job categories\n"
        f"{job_category_names}\n"
        "### Output format\n"
        "Unless otherwise instructed, leave fields blank if there is no information in the job posting.\n\n"
        "{\n"
        '   "company_name": string, # 会社名\n'
        '   "position": string, # 職種（求人タイトル）\n'
        '   "layer": string, # ["役員","管理職","一般職"] 記載がない場合は内容から推定.\n'
        '   "employment_status": string, # 雇用形態 (e.g. "正社員","契約社員", ...) 記載がない場合は内容から推定.\n'
        '   "job_category_name": string, # 職種カテゴリ. Job categoriesより選択. 記載がない場合は内容から推定.\n'
        '   "address": string, # 勤務地\n'
        '   "remote": string, # ["フルリモート","一部リモート","リモートワークなし","記載なし"]. 原則出社する必要がない場合は "フルリモート", 必ず毎日出社する必要がある場合は "リモートワークなし", それ以外の場合は "一部リモート". \n'
        '   "benefit": string, # 福利厚生についての情報\n'
        '   "holiday": string, # 休日・休暇についての情報\n'
        '   "working_hours": string, # 勤務時間についての情報\n'
        '   "trial_period": string, # 試用期間についての情報\n'
        '   "min_salary": number, # 最低年収（円）\n'
        '   "max_salary": number, # 最高年収（円）\n'
        '   "salary": string, # 1行目:年収の範囲（e.g. *** ~ ***万円）. 2行目以降:昇給、賞与、手当など、金銭に関するその他の情報\n'
        '   "smoking_prevention_measure": string, # 受動喫煙対策についての情報\n'
        '   "min_qualifications": string, # 必要なスキル・経験\n'
        '   "pfd_qualifications": string, # 歓迎されるスキル・経験\n'
        '   "ideal_profile": string, # この求人で望まれる人物像\n'
        '   "_is_application_method_written": boolean, # 応募方法が記載されているか. 具体的な応募方法は提示してはいけないため、出力に含めないこと\n'
        '   "summary": string, # 詳細な職務の内容. ここまでの項目と重複する情報を含めないように注意\n'
        '   "other": string, # その他の重要な情報\n'
        "}\n"
        "###\n"
    )


@shared_task(soft_time_limit=600, hard_time_limit=630)
def exec_job_loading(job_loading_id, source_url):
    try:
        result = JobLoadingResult(job_loading_id, source_url)

        # check url
        parsedUrl = urlparse(source_url)
        if not all([parsedUrl.scheme, parsedUrl.netloc]):
            result.save_error("URLが正しくありません。")
            raise Exception(f"Invalid URL: {source_url}")

        # fetch html body
        try:
            content = fetch_from_url(source_url, result)
        except Exception as e:
            result.add_telemetry_error_detail(str(e))
            result.set_error_message("ウェブページの取得に失敗しました。")
            e.add_note(f"Failed to fetch HTML: {source_url}")
            raise

        job_category_names = []
        jobCategories = JobCategory.objects.all()
        for jobCategory in jobCategories:
            job_category_names.append(jobCategory.name)

        # call gpt
        prompt = constructPrompt(content, job_category_names)
        openai.api_key = settings.OPENAI_API_KEY
        try:
            openai_start_time = time.time()
            logging.info(
                f"Call OpenAI API for {source_url} (jobloading_id: {job_loading_id}): {prompt}"
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ],
            )
            openai_time = round(time.time() - openai_start_time)
            logging.info(
                f"OpenAI API response for {source_url} (jobloading_id: {job_loading_id}): {openai_time} seconds, {response.model} {response.usage}"
            )
            result.set_telemetry("gpt_time", openai_time)
            result.set_telemetry("gpt_tokens_prompt", response.usage.prompt_tokens)
            result.set_telemetry(
                "gpt_tokens_completion", response.usage.completion_tokens
            )
            jobloadingJsonStr = response.choices[0].message.content
        except Exception as e:
            result.add_telemetry_error_detail(str(e))
            result.set_error_message("求人情報の解析に失敗しました。")
            # Future: HTMLをテキストのみにして再試行する
            e.add_note(f"OpenAI API call failed")
            raise

        try:
            # json として厳密でない場合をケア: 末尾のカンマを削除
            jobloadingJsonStr = re.sub(r",[\s\n]*}[\s\n]*$", "\n}\n", jobloadingJsonStr)
            jobloadingJsonStr = jobloadingJsonStr.replace("\\xa0", " ")
            # json のパース
            jobloading = json.loads(jobloadingJsonStr, strict=False)
            # json 内のnullを持つキーと、_ から始まるキーを削除
            jobloading = {
                k: v
                for k, v in jobloading.items()
                if v is not None and not k.startswith("_")
            }

            logging.info(
                f"Loaded data for {source_url} (jobloading_id: {job_loading_id}): {str(jobloading)}"
            )
        except Exception as e:
            result.add_telemetry_error_detail(str(e))
            result.add_telemetry_error_detail(f"target: {jobloadingJsonStr}")
            result.set_error_message("解析結果の取得に失敗しました。")
            e.add_note(f"Failed to parse JSON: {jobloadingJsonStr}")
            raise

        try:
            result.save_and_complete(jobloading)
        except Exception as e:
            result.add_telemetry_error_detail(str(e))
            result.add_telemetry_error_detail(f"data: {str(jobloading)}")
            result.set_error_message("解析結果の保存に失敗しました。")
            e.add_note(f"Failed to save data")
            raise

    except SoftTimeLimitExceeded as e:
        result.add_telemetry_error_detail(str(e))
        result.set_error_message("タイムアウトしました。")
        result.save_error()
        raise
    except Exception as e:
        result.save_error()
        raise
