# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter


class PetfinderPipeline:
    def open_spider(self, spider):
        self.file = open('pets_output.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        # Write CSV Header
        self.writer.writerow([
            'Pet ID', 'Name', 'Type', 'Species', 'Profile', 'Amount', 'Vaccinated', 'Dewormed', 'Spayed', 
            'Condition', 'Body', 'Color', 'Location', 'Posted', 'Price', 'Uploader Type', 'Uploader Name', 'Status'
        ])
    
    def process_item(self, item, spider):
        self.writer.writerow([
            item['pet_id'], item['name'], item['type'], item['species'], item['profile'], item['amount'],
            item['vaccinated'], item['dewormed'], item['spayed'], item['condition'], item['body'],
            item['color'], item['location'], item['posted'], item['price'],
            item['uploader_type'], item['uploader_name'], item['status']
        ])
        return item
    
    def close_spider(self, spider):
        self.file.close()
