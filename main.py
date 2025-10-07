from dotenv import load_dotenv
from llm import ListingEvaluatorLLMClient
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.craigslistspider import CraigslistSpider

load_dotenv()

def run_spider():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'scraper.scraper.settings')
    settings = get_project_settings()
    settings.update({
        "FEEDS": {
            "test.json": {
                "format": "json",
                "overwrite": True,
            }
        }
    })

    process = CrawlerProcess(settings)
    process.crawl(CraigslistSpider)
    process.start()


def main():
    # client = ListingEvaluatorLLMClient()

    # l1 = {'title': 'Ridley Kanzo Fast Small-SRAM RED/EAGLE MULLET', 'post_id': 7884093416, 'attribute_group': {'bicycle type': 'gravel', 'frame size': 'Small (53-54cm)', 'wheel size': '700C', 'bicycle frame material': 'carbon fiber', 'suspension': 'none (rigid)', 'brake type': 'disc (hydraulic)', 'handlebar type': 'drop', 'electric assist': 'none', 'condition': 'excellent', 'make / manufacturer': 'Ridley', 'model name / number': 'Kanzo Fast'}, 'updated_at': '2025-09-25 09:06', 'content': "This listing is for one of my all-time favorite bikes. It introduced me to gravel riding, but I now have a full-blown gravel and a new all-road bike, and I don't have room for it anymore. This is a custom-built, one-of-a-kind combination of high-end parts and custom-colored tires and bottle cages. Tire clearance tops out at 36mm but that was plenty for most fast dry gravel routes that I run. I would recommend getting more clearance if you want to ride deep thick mud like a Lauf Siegla.     Here'...", 'url': 'https://sfbay.craigslist.org/eby/bik/d/oakland-ridley-kanzo-fast-small-sram/7884093416.html'}
    # l2 = {'title': 'Seven 622SL 52/54cm', 'post_id': 7881931642, 'attribute_group': {'bicycle type': 'road', 'frame size': '52cm', 'wheel size': '700C', 'bicycle frame material': 'titanium', 'brake type': 'disc (hydraulic)', 'handlebar type': 'drop', 'make / manufacturer': 'Seven', 'model name / number': '622SL'}, 'updated_at': '2025-09-25 12:58', 'content': 'Custom Seven 622sl, carbon and titanium lugs. Argen tubeset. Built summer of 2021. Fits 32mm tires, currently fitted with 27mm (measured) Continental GP5k.     Handbuilt wheels, Bitex hubs, Pacenti Forza rims, 28/28 hole.     Fitted with a 95mm stem, 40cm Zipp Service Course compact bars, matching Zipp seatpost (zero setback)    Specialized Power Expert, 143mm    160mm rotors, TRP centerlock. New pads, rotors have tons of life    New Zipp Service Course bar tape    Shimano Ultegra 8000 11-speed ...', 'url': 'https://sfbay.craigslist.org/eby/bik/d/oakland-seven-622sl-52-54cm/7881931642.html'}
    # l3 = {'title': 'Specialized Ruby/Roubaix Sport', 'post_id': 7871271922, 'attribute_group': {'bicycle type': 'road', 'frame size': '54cm', 'wheel size': '700C', 'bicycle frame material': 'carbon fiber', 'suspension': 'other/unknown', 'brake type': 'disc (mechanical)', 'handlebar type': 'drop', 'electric assist': 'none', 'condition': 'like new', 'make / manufacturer': 'Specialized', 'model name / number': 'Ruby / Roubaix'}, 'updated_at': '2025-09-27 16:52', 'content': 'A few years old but lightly ridden and very well maintained. Was tuned up recently with new disc brake rotors, brake pads and new tires (32’ and tubeless for a super comfy road ride). We’ve been doing more mountain biking lately and as capable as this is on gravel it’s not ridden as much as we’d like so making space in the garage.       From the original description of the bike:    Specialized Ruby Sport Features    Looking for a bike to explore the road less traveled, while also keeping room in...', 'url': 'https://sfbay.craigslist.org/sfc/bik/d/san-francisco-specialized-ruby-roubaix/7871271922.html'}
    # l4 = {'title': '53cm Taylor steel road bike 27sp Shimano -', 'post_id': 7871384569, 'attribute_group': {'bicycle type': 'road', 'frame size': '53cm', 'wheel size': '700C', 'bicycle frame material': 'steel', 'make / manufacturer': 'Taylor'}, 'updated_at': '2025-09-28 00:03', 'content': "Here is your chance to own something unique – a custom made steel frame by Paul Taylor. (one of the top artisan frame builders in the country and winner of multiple NAHBS awards). Paul is from Australia, which is why there is a kangaroo logo on his frames. Beautiful paint job with white to vibrant blue fades. Frame has a more upright, endurance, oriented, geometry.    It's built up with a Shimano 3x9 speed Shimano 105 drivetrain with STI shifters. Clincher wheels are perfectly straight and spin ...", 'url': 'https://sfbay.craigslist.org/sfc/bik/d/san-francisco-53cm-taylor-steel-road/7871384569.html'}
    # l5 = {'title': '54cm Trek Madone 5.2 H2 KVF Carbon Road Bike - Shimano Ultegra 11sp', 'post_id': 7841803553, 'attribute_group': {'frame size': '54cm', 'make / manufacturer': 'Trek', 'model name / number': 'Madone 5.2 H2 KVF', 'serial number': 'WTU007CT0098J'}, 'updated_at': '2025-09-28 00:03', 'content': 'This is a 2015 Trek Madone 5.2 with Trek’s H2 geometry, featuring a featherlight 500 Series OCLV carbon monocoque frame and fork. Retailed originally for around $4,100 — now priced to move at $1,475.    🔹 Size: 54cm (ideal for riders 5’8” to 5’10”)  🔹 Drivetrain: Full 2x11 Shimano Ultegra groupset (shifters, derailleurs, brakes, crankset)  🔹 Crankset: 50/34t compact  🔹 Cassette: 11-30t  🔹 Wheelset: HED Ardennes clinchers — smooth and true  🔹 Frame Tech: KVF (Kammtail Virtual Foil) aero tube prof...', 'url': 'https://sfbay.craigslist.org/sfc/bik/d/san-francisco-54cm-trek-madone-52-h2/7841803553.html'}

    # listings = [l1, l2, l3, l4, l5]

    # evaluated = client.evaluate_listings(listings)

    # print(evaluated)

    run_spider()

if __name__ == "__main__":
    main()
