from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


def run_scraper(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python", script_name])


def schedule_jobs():
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_scraper, 'cron', args=['scraper.py'], day_of_week='mon-fri', hour='0,1,8,12,16,20')
    scheduler.add_job(run_scraper, 'cron', args=['scraper1.py'], day_of_week='mon-fri', hour='0,1,8,12,16,20')

    scheduler.add_job(run_scraper, 'cron', args=['scraper.py'], day_of_week='sat', hour='0-23')
    scheduler.add_job(run_scraper, 'cron', args=['scraper1.py'], day_of_week='sat', hour='0-23')

    scheduler.add_job(run_scraper, 'cron', args=['scraper.py'], day_of_week='sun', hour='0-23')
    scheduler.add_job(run_scraper, 'cron', args=['scraper1.py'], day_of_week='sun', hour='0-23')

    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    schedule_jobs()
