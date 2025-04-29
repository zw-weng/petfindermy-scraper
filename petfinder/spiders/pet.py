import scrapy
from petfinder.items import PetfinderItem


class PetSpider(scrapy.Spider):
    name = "pet"
    allowed_domains = ["petfinder.my"]
    # start_urls = ["https://www.petfinder.my/pets/93086/"]
    
    def start_requests(self):
        for pet_id in range(71001, 88252):  # from 71001 to 105000 inclusive
            url = f'https://www.petfinder.my/pets/{pet_id}/'
            yield scrapy.Request(url, callback=self.parse, meta={'pet_id': pet_id})

    def parse(self, response):
        pet_id = response.meta['pet_id']

        if "Pet Not Found" in response.text or response.status == 404:
            self.logger.info(f"Pet ID {pet_id} not found.")
            return

        item = PetfinderItem()
        item['pet_id'] = pet_id

        # Extract pet name
        pet_title_tag = response.css('div.pet_title')
        item['name'] = pet_title_tag.xpath('.//td[@align="center"]/text()').get("").strip() if pet_title_tag else "N/A"

        # Extract details from info table
        info_table = response.css('table.pet_box')
        pet_details = {}
        
        if info_table:
            rows = info_table.css('tr')
            for row in rows:
                cols = row.css('td')
                if len(cols) >= 2:
                    key_tag = cols[0].css('b::text').get()
                    if key_tag:
                        key = key_tag.strip().replace(":", "")
                        value = cols[1].xpath('string()').get().strip()
                        pet_details[key] = value

        # Type and Species
        item['type'] = next(iter(pet_details.keys()), "N/A")
        item['species'] = pet_details.get(item['type'], "N/A")

        # Add other details to item
        item['profile'] = pet_details.get('Profile', 'N/A')
        item['amount'] = pet_details.get('Amount', 'N/A')
        item['vaccinated'] = pet_details.get('Vaccinated', 'N/A')
        item['dewormed'] = pet_details.get('Dewormed', 'N/A')
        item['spayed'] = pet_details.get('Spayed', 'N/A')
        item['condition'] = pet_details.get('Condition', 'N/A')
        item['body'] = pet_details.get('Body', 'N/A')
        item['color'] = pet_details.get('Color', 'N/A')
        item['location'] = pet_details.get('Location', 'N/A')
        item['posted'] = pet_details.get('Posted', 'N/A')

        # Price/Adoption Fee
        adoption_fee = "N/A"
        rows = info_table.css('tr')
        for row in rows:
            cols = row.css('td')
            if len(cols) >= 2:
                key_tag = cols[0].css('b::text').get()
                if key_tag and 'Adoption Fee' in key_tag:
                    fee_tag = cols[1].css('b::text').get()
                    if fee_tag:
                        adoption_fee = fee_tag.strip()
                    else:
                        adoption_fee = cols[1].xpath('string()').get().strip()
        item['price'] = adoption_fee

        # Uploader Type and Name
        uploader_td = response.xpath('//td[@align="left" and @width="130" and @valign="middle"]')
        uploader_type = "N/A"
        uploader_name = "N/A"

        if uploader_td:
            uploader_type = uploader_td.css('font::text').get("").strip()
            uploader_name_tag = uploader_td.css('a.darkgrey::text').get()
            uploader_name = uploader_name_tag.strip() if uploader_name_tag else "N/A"

        item['uploader_type'] = uploader_type
        item['uploader_name'] = uploader_name

        # Status
        status_tag = response.css('div.pet_label::text').get()
        item['status'] = status_tag.strip() if status_tag else "N/A"

        yield item