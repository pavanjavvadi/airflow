import boto3
from botocore.exceptions import NoCredentialsError
from airflow import DAG
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import time

date = datetime.now()
def take_screenshot(url: str, ti):
    driver = webdriver.Chrome('/home/pavan/airflow/airflow/chromedriver')
    driver.get(url)
    print(driver.title)
    button=driver.find_element_by_id("onetrust-accept-btn-handler")
    button.send_keys(Keys.RETURN)
    time.sleep(1)
    div=driver.find_element_by_id("age_select_day")
    div.send_keys("30")
    time.sleep(1)
    div=driver.find_element_by_id("age_select_month")
    div.send_keys("November")
    time.sleep(1)
    div=driver.find_element_by_id("age_select_year")
    div.send_keys("1980")
    time.sleep(1)
    button=driver.find_element_by_id("age_confirm_btn")
    button.send_keys(Keys.RETURN)
    time.sleep(1)
    ss = driver.save_screenshot(f'/home/pavan/airflow/airflow/ss-{date}.png')
    driver.close()
    ti.xcom_push(key='screenshot', value=ss)
    return ss

def save_file(ss, bucket_name: str, file_name: str):
    ACCESS_KEY = 'AKIAVR*************************'
    SECRET_KEY = 'ErZ***********************************'
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(ss, bucket_name, file_name)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['pavan.javvadi04@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    'screenshot',
    default_args=default_args,
    description='allow user into the website if user age is > 18',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    take_ss = PythonOperator(
        task_id='take_screenshot',
        python_callable=take_screenshot,
        op_kwargs={"url": "https://www.captainmorgan.com/en-row/"}
    )

    save_images = PythonOperator(
        task_id='save_image',
        python_callable=save_file,
        op_kwargs={'ss': f'/home/pavan/airflow/airflow/ss-{date}.png', 'bucket_name': 'ubuntu-airflow', 'file_name': f'screenshot-{date}.png'}
    )
    
take_ss >> save_images
# take_ss
