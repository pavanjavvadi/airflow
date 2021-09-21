import requests
from typing import List, Dict
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['pavan.javvadi04@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['etl_pipeline'])
def perform_etl_pipeline():
    
    @task
    def extract_json(url: str) -> List:
        json_data = requests.get(url)
        output_data = json_data.json()
        return output_data

    @task
    def transform(posts: List) -> Dict:
        count = 0
        for post in posts:
            if post['userId'] == 1:
                count = count + 1

        return {'count': count}

    @task
    def load(count: int) -> None:
        print(f"Number of posts made by user1 are: {count}")

    fetched_data = extract_json('https://jsonplaceholder.typicode.com/posts')
    count_numb = transform(fetched_data)
    load(count_numb['count'])

etl_dag = perform_etl_pipeline()