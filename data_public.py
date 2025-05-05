from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time


# ChromeDriver
chromedriver_path = r"C:\Users\User\Desktop\projet_fin_d'annee\chromedriver-win64\chromedriver.exe"


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")


service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "http://www.lynx-erp.tn/lynxerp/#/home/ho-accueil-page"


try:
    print("Chargement de la page...")
    driver.get(url)


    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


    #Simuler des comportements humains pour contourner les protections anti-bot
    print("Simulation de comportements humains...")
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)


    print("Attente du contenu dynamique...")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.home-body-seperator"))
        )
        print("Sélecteur home-body-seperator trouvé.")
    except:
        print("Sélecteur home-body-seperator non trouvé, mais on continue...")


    # Section "À propos de nous"
    print("Extraction de la section 'À propos de nous'...")
    about_us_subtitle = driver.execute_script("""
        const card = document.querySelector('lyx-card .card-title');
        return card?.querySelector('h3')?.textContent.trim() || 'Sous-titre non trouvé';
    """)
    about_us_items = driver.execute_script("""
        const card = document.querySelector('lyx-card .card-description');
        const aboutUsList = card?.querySelector('ul.lyx-list-borderless');
        if (aboutUsList) {
            const items = Array.from(aboutUsList.querySelectorAll('li'))
                .map(li => {
                    // Récupérer le texte complet du <li> (y compris les balises <b>)
                    let fullText = li.textContent.trim();
                    if (!fullText) return null; // Ignorer les <li> vides
                    // Récupérer les textes des balises <b> à l'intérieur
                    const boldItems = Array.from(li.querySelectorAll('b')).map(b => b.textContent.trim());
                    return { fullText: fullText, boldItems: boldItems };
                })
                .filter(item => item !== null); // Filtrer les éléments vides
            return items;
        }
        return [];
    """)


    #Section Solution
    print("Extraction de la section 'Solution'...")
    solution_title = driver.execute_script("""
        const seperator = document.querySelector('div.home-body-seperator');
        return seperator?.querySelector('h2.lyx-center-text')?.textContent.trim() || 'Titre non trouvé';
    """)
    solution_subtitle = driver.execute_script("""
        const card = Array.from(document.querySelectorAll('lyx-card'))[1]; // Deuxième lyx-card (après "À propos de nous")
        return card?.querySelector('div.card-title h3')?.textContent.trim() || 'Sous-titre non trouvé';
    """)


    solution_description = driver.execute_script("""
        const card = Array.from(document.querySelectorAll('lyx-card'))[1];
        const description = card?.querySelector('div.card-description h5 p');
        return description?.textContent.trim() || 'Description non trouvée';
    """)


    solution_modules = driver.execute_script("""
        const card = Array.from(document.querySelectorAll('lyx-card'))[1];
        const moduleList = card?.querySelector('div.card-description ul.lyx-list-borderless');
        if (moduleList) {
            const items = Array.from(moduleList.querySelectorAll('li'))
                .map(li => li.textContent.trim())
                .filter(text => text !== ''); // Filtrer les éléments vides
            return items;
        }
        return [];
    """)


    #Section Avantages de Lynx-ERP
    print("Extraction de la section 'Avantages de Lynx-ERP'...")
    advantages = driver.execute_script("""
        const advantagesSection = document.querySelector('div.home-body-solutions');
        return advantagesSection
            ? Array.from(advantagesSection.querySelectorAll('lyx-card-image')).map(card => {
                  const contentVertical = card.querySelector('div.lyx-card-image-content-vertical');
                  if (!contentVertical) return null;


                  const titleDiv = contentVertical.querySelector('div.lyx-card-image-title');
                  const advantageTitle = titleDiv?.querySelector('h3')?.textContent.trim() || 'Titre non trouvé';


                  const descriptionDiv = contentVertical.querySelector('div.lyx-card-image-description');
                  const advantageDescription = descriptionDiv?.querySelector('p')?.textContent.trim() || 'Description non trouvée';


                  return { title: advantageTitle, description: advantageDescription };
              }).filter(advantage => advantage)
            : [];
    """)


    #Section Lynx-ERP Solution
    print("Extraction de la section 'Lynx-ERP Solution'...")
    lynx_erp_title = driver.execute_script("""
        const lynxErpSection = document.querySelector('div.home-body-solutions-product');
        if (lynxErpSection) {
            const titleDiv = lynxErpSection.querySelector('div.card-title');
            return titleDiv?.querySelector('h3')?.textContent.trim() || 'Titre non trouvé';
        }
        return 'Titre non trouvé';
    """)
    lynx_erp_content_solution = driver.execute_script("""
        const lynxErpSection = document.querySelector('div.home-body-solutions-product');
        let result = [];
        if (lynxErpSection) {
            const descriptionH5 = lynxErpSection.querySelector('h5');
            if (descriptionH5) {
                const paragraphs = [];
                let currentParagraph = [];
                for (const child of descriptionH5.childNodes) {
                    if (child.tagName && child.tagName.toLowerCase() === 'br') {
                        if (currentParagraph.length) {
                            paragraphs.push(currentParagraph.join(' ').trim());
                            currentParagraph = [];
                        }
                    } else {
                        const text = child.textContent.trim();
                        if (text) currentParagraph.push(text);
                    }
                }
                if (currentParagraph.length) paragraphs.push(currentParagraph.join(' ').trim());
                result = paragraphs.length ? paragraphs : ['Description non trouvée'];
            }
        }
        return result;
    """)


    #Section Contact
    print("Extraction de la section 'Contact'...")
    #Section Tel
    contact_title = driver.execute_script("""
        const contactSeperator = document.querySelector('div.home-body-seperator');
        return contactSeperator?.querySelector('h2.lyx-center-text')?.textContent.trim() || 'Contact (titre non trouvé)';
    """)
    contact_subtitle = driver.execute_script("""
        const contactSection = document.querySelector('div.home-body-contact');
        return contactSection?.querySelector('h4')?.textContent.trim() || 'Sous-titre non trouvé';
    """)
    contact_availability = driver.execute_script("""
        const contactSection = document.querySelector('div.home-body-contact');
        return contactSection?.querySelector('h5')?.textContent.trim() || 'Horaires non trouvés';
    """)
    contact_items = driver.execute_script("""
        const contactSection = document.querySelector('div.home-body-contact');
        if (contactSection) {
            const contactList = contactSection.querySelector('ul.lyx-list');
            return contactList
                ? Array.from(contactList.querySelectorAll('li')).map(li => li.textContent.trim())
                : ['Aucun contact trouvé'];
        }
        return ['Section Contact non trouvée'];
    """)
    #Section "Email"
    print("Extraction de la section 'Email'...")
    additional_contact_card = driver.execute_script("""
        const cards = document.querySelectorAll('lyx-card[direction="vertical"][iconcolor="primary"][titlecolor="primary"]');
        if (cards.length > 1) {
            const card = cards[1]; // Prendre la deuxième carte
            const header = card.querySelector('div.lyx-card-header');
            const cardBody = card.querySelector('section.lyx-card-body');
            if (cardBody) {
                const title = header?.querySelector('h4')?.textContent.trim() || 'Titre non trouvé';
                const subtitle = cardBody.querySelector('h5')?.textContent.trim() || 'Sous-titre non trouvé';
                const list = cardBody.querySelector('ul.lyx-list');
                const items = list
                    ? Array.from(list.querySelectorAll('li'))
                        .map(li => li.textContent.trim())
                        .filter(item => item) // Filtrer les éléments vides
                    : ['Aucun élément trouvé'];
                return { title, subtitle, items };
            }
        }
        return { title: 'Carte non trouvée', subtitle: 'Sous-titre non trouvé', items: ['Aucun élément trouvé'] };
    """)


    #Section "Localisation"
    print("Ajout de la section 'Localisation' avec des données statiques...")
    location_data = {
        "placeName": "Pépinière d'entreprises",
        "address": "RQP3+9M9, Express Rocade Nr 11, Sakiet Ezzit 3021",
        "mapUrl": "https://www.google.com/maps/place/P%C3%A9pini%C3%A8re+d'entreprises/@34.835914,10.754237,19z/data=!4m6!3m5!1s0x1301d178035906ab:0x16623f57fb73f056!8m2!3d34.8359141!4d10.7542366!16s%2Fg%2F11b742559b?hl=en&entry=ttu&g_ep=EgoyMDI1MDQwNy4wIKXMDSoASAFQAw%3D%3D",
         "description": "Située à 10 km de la route de Tunis"}


    #Sauvegardage
    print("Sauvegarde des données dans data_public.txt...")
    with open('data_public.txt', 'w', encoding='utf-8') as f:
        #Section "À propos de nous"
        f.write("Section: À propos de nous\n")
        if about_us_items:
            for item in about_us_items:
                f.write(f"- {item['fullText']}\n")
                if item['boldItems']:
                    f.write("  Bold Items:\n")
                    for bold in item['boldItems']:
                        f.write(f"    - {bold}\n")
        else:
            f.write("- Aucun élément trouvé\n")
        f.write("\n")


        #Section "module"
        f.write("Section: MODULES\n")
        f.write(f" {solution_description}\n")
        f.write("Modules:\n")
        if solution_modules:
            for module in solution_modules:
                f.write(f"- {module}\n")
        else:
            f.write("- Aucun module trouvé\n")
        f.write("\n")


        #Section "Avantages de Lynx-ERP"
        f.write("Section: Avantages de Lynx-ERP\n")
        if advantages:
            for advantage in advantages:
                f.write(f"Advantage: {advantage['title']}\n")
                f.write(f"{advantage['description']}\n")
        else:
            f.write("Aucun avantage trouvé\n")
        f.write("\n")


        #Section "Lynx-ERP Solution"
        f.write("Section: Lynx-ERP Solution\n")
        f.write("\n")
        if lynx_erp_content_solution:
            for content in lynx_erp_content_solution:
                f.write(f"- {content}\n")
        else:
            f.write("- Aucun contenu trouvé\n")
        f.write("\n")


        #Section "Contact"
        f.write("Section: Contact\n")
        f.write(f"Title: {contact_title}\n")
        f.write(f"Subtitle: {contact_subtitle}\n")
        f.write(f"Availability: {contact_availability}\n")
        f.write("Contacts:\n")
        if contact_items:
            for item in contact_items:
                f.write(f"- {item}\n")
        else:
            f.write("- Aucun contact trouvé\n")


        f.write("Email:\n")
        f.write(f"Card Title: {additional_contact_card['title']}\n")
        f.write(f"Card Subtitle: {additional_contact_card['subtitle']}\n")
        f.write("Card Items:\n")
        for item in additional_contact_card['items']:
            f.write(f"- {item}\n")
        f.write("\n")


        #Section "Localisation"
        f.write("Section: Localisation\n")
        f.write(f"Place Name: {location_data['placeName']}\n")
        f.write(f"Address: {location_data['address']}\n")
        f.write(f"Map URL: {location_data['mapUrl']}\n")
        f.write(f"Description: {location_data['description']}\n")
        f.write("\n")


    print("Données sauvegardées dans ..public_data.txt")


except Exception as e:
    print(f"Une erreur s'est produite : {str(e)}")     


finally:
   
    print("Fermeture du navigateur...")
    driver.quit()
