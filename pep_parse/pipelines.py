import csv
from pathlib import Path
import datetime as dt


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.status = {}

    def process_item(self, item, spider):
        self.status[item['status']] = self.status.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = results_dir / f'status_summary_{now}.csv'
        summary = sum(self.status.values())
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(self.status.items())
            writer.writerow(('Total', summary))
