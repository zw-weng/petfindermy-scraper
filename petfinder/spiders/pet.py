import scrapy
from petfinder.items import PetfinderItem


class PetSpider(scrapy.Spider):
    name = "pet"
    allowed_domains = ["petfinder.my"]
    # start_urls = ["https://www.petfinder.my/pets/93086/"]
    
    def start_requests(self):
        for pet_id in range(71001, 71003):  # from 71001 to 105000 inclusive
            url = f'https://www.petfinder.my/pets/{pet_id}/'
            yield scrapy.Request(url, callback=self.parse, meta={'pet_id': pet_id})

    def parse(self, response):
        pet_id = response.meta['pet_id']

        # Pet not found
        if "Pet Not Found" in response.text or response.status == 404:
            self.logger.info(f"Pet ID {pet_id} not found.")
            return

        def extract_with_css(query):
            return response.css(query).get(default="N/A").strip()

        item = PetfinderItem()

        item['pet_id'] = pet_id
        item['name'] = extract_with_css('div.pet_title td[align="center"]::text')

        # Default N/A for all fields
        fields = [
            'type', 'species', 'profile', 'amount', 'vaccinated', 'dewormed',
            'spayed', 'condition', 'body', 'color', 'location', 'posted', 'price',
            'uploader_type', 'uploader_name', 'status'
        ]
        for field in fields:
            item[field] = "N/A"

        # Correct parsing of pet profile table
        rows = response.xpath('//table[@class="pet_box"]//td[@valign="middle"]//table//tr')

        for row in rows:
            label = row.xpath('.//td[1]/b/text()').get()
            value = row.xpath('.//td[2]//text()').get()

            if label and value:
                label = label.strip()
                value = value.strip()

                if label in ["Dog", "Cat", "Rabbit", "Hamster", "Bird", "Turtle", "Fish", "Reptile"]:
                    item['type'] = label
                    item['species'] = value
                elif label == "Profile":
                    item['profile'] = value
                elif label == "Amount":
                    item['amount'] = value
                elif label == "Vaccinated":
                    item['vaccinated'] = value
                elif label == "Dewormed":
                    item['dewormed'] = value
                elif label == "Spayed" or label == "Neutered":  # some pages use "Neutered"
                    item['spayed'] = value
                elif label == "Condition":
                    item['condition'] = value
                elif label == "Body":
                    item['body'] = value
                elif label == "Color":
                    item['color'] = value
                elif label == "Location":
                    item['location'] = value
                elif label == "Posted":
                    item['posted'] = value
                elif label == "Adoption Fee":
                    item['price'] = value

        # Uploader
        item['uploader_type'] = extract_with_css('td[width="130"] font::text')
        item['uploader_name'] = extract_with_css('td[width="130"] a.darkgrey::text')

        # Status (Adopted / For Adoption)
        item['status'] = extract_with_css('div.pet_label::text')

        yield item