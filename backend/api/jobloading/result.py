import time
from ..models import JobLoading

class JobLoadingResult:
    def __init__(self, jobloading_id, source_url):
        self.jobloading_id = jobloading_id
        self.source_url = source_url
        self.start_time = time.time()
        self.error_message = ""
        self.telemetries = {
            "telemetry_fetch_method": "",
            "telemetry_scraping_time": None,
            "telemetry_html_processing_names": [],
            "telemetry_html_processing_results": [],
            "telemetry_gpt_time": None,
            "telemetry_gpt_tokens_prompt": None,
            "telemetry_gpt_tokens_completion": None,
            "telemetry_error_detail": "",
            "telemetry_total_time": None
        }

    def save_and_complete(self, jobloading_json: dict):
        self.set_telemetry('total_time', round(time.time() - self.start_time))
        JobLoading.objects.filter(id=self.jobloading_id).update(
            is_completed=True,
            **jobloading_json,
            **self.telemetries,
        )
    

    def save_error(self):
        self.set_telemetry('total_time', round(time.time() - self.start_time))
        JobLoading.objects.filter(id=self.jobloading_id).update(
            is_error=True,
            error_message=self.error_message,
            **self.telemetries,
        )

    def set_error_message(self, error_message: str):
        self.error_message = error_message
    
    def set_telemetry(self, key: str, value: any):
        self.telemetries[f'telemetry_{key}'] = value
    
    def add_telemetry_error_detail(self, error_detail: str):
        self.telemetries['telemetry_error_detail'] += f'{error_detail}\n'
    
    def add_telemetry_html_processing(self, name: str, chars: int):
        self.telemetries['telemetry_html_processing_names'].append(name)
        self.telemetries['telemetry_html_processing_results'].append(chars)
