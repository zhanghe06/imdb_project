import csv
import json
import socket

import requests
import socks
import urllib3
from lxml import etree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# socks代理配置
PROXY_IP = '127.0.0.1'
PROXY_PORT = 1086

socks.set_default_proxy(socks.SOCKS5, PROXY_IP, PROXY_PORT)
socket.socket = socks.socksocket

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}


def get_imdb_id(title):
    """根据影片名称查询编号"""
    url_pattern = 'https://v2.sg.media-imdb.com/suggestion/{k}/{v}.json'
    # 关键词规则
    title = title.replace(':', '_')
    title = title.replace('\'', '_')
    title = title.replace(',', '_')
    title = title.replace('(', '_')
    title = title.replace(')', '_')
    title = title.replace('-', '_')
    title = title.replace(' ', '_')
    title = title.replace('.', '')
    title = title.replace('__', '_')
    title = title.strip('_')
    title = title.lower()
    url = url_pattern.format(k=title[:1], v=title[:20].strip('_'))
    print('movie search url: %s' % url)
    res = requests.get(url, headers=headers, verify=False).json()
    imdb_id = ''
    for suggestion in res.get('d', []):
        imdb_id = suggestion['id']
        break
    print('movie imdb id: %s' % imdb_id)
    return imdb_id


def get_imdb_info(imdb_id):
    """根据编号获取影片详情"""
    url_pattern = 'https://www.imdb.com/title/{imdb_id}/'
    url = url_pattern.format(imdb_id=imdb_id)
    print('movie detail info url: %s' % url)

    imdb_info = {
        'title': '',  # 标题
        'time': '',  # 时长
        'release_time': '',  # 首映时间
        'intro': '',  # 简介
        'director': '',  # 导演
        'writers': '',  # 编剧
        'stars': '',  # 明星
        'genre': '',  # 类型
        'url': '',  # 海报链接
    }

    html = requests.get(url, headers=headers, verify=False).text
    text = etree.HTML(html)

    imdb_info['title'] = ''.join(text.xpath('//h1[contains(@class, "eKrKux")]/text()'))
    imdb_info['release_time'] = ''.join(text.xpath('//ul[contains(@class, "kqWovI")]/li[1]/span/text()'))
    imdb_info['time'] = ''.join(text.xpath('//ul[contains(@class, "kqWovI")]/li[3]/text()'))
    imdb_info['intro'] = ''.join(text.xpath('//span[contains(@class, "gXUyNh")]/text()'))
    imdb_info['director'] = '|'.join(text.xpath('//div[contains(@class, "fjLeDR")]/ul/li[1]//ul/li//text()'))
    imdb_info['writers'] = '|'.join(text.xpath('//div[contains(@class, "fjLeDR")]/ul/li[2]//ul/li//text()'))
    imdb_info['stars'] = '|'.join(text.xpath('//div[contains(@class, "fjLeDR")]/ul/li[3]//ul/li//text()'))
    imdb_info['genre'] = '|'.join(text.xpath('//div[contains(@class, "bMBIRz")]//ul/li//text()'))
    imdb_info['url'] = '|'.join(text.xpath('//div[contains(@class, "fBcbjp")]//img/@src'))

    print(json.dumps(imdb_info, indent=4, ensure_ascii=False))
    return imdb_info


def write_csv():
    header = []
    csv_file = open('imdb.csv', 'a')
    csv_write = csv.writer(csv_file, dialect='excel')
    csv_write.writerow(header)
    csv_file.close()


def run():
    title_list = [
        "Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)",
        "Seven (Se7en) (1995)",
        "Usual Suspects, The (1995)",
        "Postino, Il (1994)",
        "French Twist (Gazon maudit) (1995)",
        "White Balloon, The (1995)",
        "Antonia's Line (1995)",
        "Rumble in the Bronx (1995)",
        "Birdcage, The (1996)",
        "Brothers McMullen, The (1995)",
        "Doom Generation, The (1995)",
        "Net, The (1995)",
        "To Wong Foo, Thanks for Everything! Julie Newmar (1995)",
        "Dolores Claiborne (1994)",
        "Eat Drink Man Woman (1994)",
        "Madness of King George, The (1994)",
        "Professional, The (1994)",
        "Three Colors: Red (1994)",
        "Three Colors: Blue (1993)",
        "Three Colors: White (1994)",
        "Santa Clause, The (1994)",
        "Shawshank Redemption, The (1994)",
        "Crow, The (1994)",
        "Lion King, The (1994)",
        "Mask, The (1994)",
        "Faster Pussycat! Kill! Kill! (1965)",
        "Brother Minister: The Assassination of Malcolm X (1994)",
        "Firm, The (1993)",
        "Fugitive, The (1993)",
        "Hudsucker Proxy, The (1994)",
        "Robert A. Heinlein's The Puppet Masters (1994)",
        "Ref, The (1994)",
        "Remains of the Day, The (1993)",
        "Nightmare Before Christmas, The (1993)",
        "Silence of the Lambs, The (1991)",
        "Aristocats, The (1970)",
        "Truth About Cats & Dogs, The (1996)",
        "Horseman on the Roof, The (Hussard sur le toit, Le) (1995)",
        "Wallace & Gromit: The Best of Aardman Animation (1996)",
        "Haunted World of Edward D. Wood Jr., The (1995)",
        "Rock, The (1996)",
        "Independence Day (ID4) (1996)",
        "Cable Guy, The (1996)",
        "Frighteners, The (1996)",
        "Spitfire Grill, The (1996)",
        "Godfather, The (1972)",
        "Supercop (1992)",
        "Wizard of Oz, The (1939)",
        "Love Bug, The (1969)",
        "Sound of Music, The (1965)",
        "Lawnmower Man, The (1992)",
        "Unhook the Stars (1996)",
        "Long Kiss Goodnight, The (1996)",
        "Ghost and the Darkness, The (1996)",
        "Willy Wonka and the Chocolate Factory (1971)",
        "Fish Called Wanda, A (1988)",
        "Monty Python's Life of Brian (1979)",
        "Return of the Pink Panther, The (1974)",
        "Abyss, The (1989)",
        "Manon of the Spring (Manon des sources) (1986)",
        "Monty Python and the Holy Grail (1974)",
        "Wrong Trousers, The (1993)",
        "Cinema Paradiso (1988)",
        "Empire Strikes Back, The (1980)",
        "Princess Bride, The (1987)",
        "Good, The Bad and The Ugly, The (1966)",
        "Clockwork Orange, A (1971)",
        "Return of the Jedi (1983)",
        "GoodFellas (1990)",
        "Army of Darkness (1993)",
        "Blues Brothers, The (1980)",
        "Godfather: Part II, The (1974)",
        "Grand Day Out, A (1992)",
        "Right Stuff, The (1983)",
        "Sting, The (1973)",
        "Terminator, The (1984)",
        "Graduate, The (1967)",
        "Nikita (La Femme Nikita) (1990)",
        "Bridge on the River Kwai, The (1957)",
        "Shining, The (1980)",
        "M*A*S*H (1970)",
        "Unbearable Lightness of Being, The (1988)",
        "Room with a View, A (1986)",
        "Pink Floyd - The Wall (1982)",
        "Bram Stoker's Dracula (1992)",
        "Nightmare on Elm Street, A (1984)",
        "Mirror Has Two Faces, The (1996)",
        "Star Trek: The Wrath of Khan (1982)",
        "Beavis and Butt-head Do America (1996)",
        "Last of the Mohicans, The (1992)",
        "Kolya (1996)",
        "Jungle2Jungle (1997)",
        "Devil's Own, The (1997)",
        "Fifth Element, The (1997)",
        "Shall We Dance? (1996)",
        "Lost World: Jurassic Park, The (1997)",
        "Pillow Book, The (1995)",
        "When the Cats Away (Chacun cherche son chat) (1996)",
        "Hunt for Red October, The (1990)",
        "unknown",
        "Full Monty, The (1997)",
        "Up Close and Personal (1996)",
        "River Wild, The (1994)",
        "Time to Kill, A (1996)",
        "English Patient, The (1996)",
        "Promesse, La (1996)",
        "Ice Storm, The (1997)",
        "Mrs. Brown (Her Majesty, Mrs. Brown) (1997)",
        "Devil's Advocate, The (1997)",
        "Rainmaker, The (1997)",
        "Wings of the Dove, The (1997)",
        "3 Ninjas: High Noon At Mega Mountain (1998)",
        "As Good As It Gets (1997)",
        "187 (1997)",
        "Edge, The (1997)",
        "Game, The (1997)",
        "How to Be a Player (1997)",
        "House of Yes, The (1997)",
        "Man Who Knew Too Little, The (1997)",
        "Apostle, The (1997)",
        "Prophecy II, The (1998)",
        "Wedding Singer, The (1998)",
        "Client, The (1994)",
        "Assignment, The (1997)",
        "Wonderland (1997)",
        "Bridges of Madison County, The (1995)",
        "Houseguest (1994)",
        "Heavyweights (1994)",
        "Tales From the Crypt Presents: Demon Knight (1995)",
        "Adventures of Priscilla, Queen of the Desert, The (1994)",
        "Flintstones, The (1994)",
        "Age of Innocence, The (1993)",
        "Man Without a Face, The (1993)",
        "Three Musketeers, The (1993)",
        "Little Rascals, The (1994)",
        "Brady Bunch Movie, The (1995)",
        "Close Shave, A (1995)",
        "Nutty Professor, The (1996)",
        "Very Brady Sequel, A (1996)",
        "Tales from the Crypt Presents: Bordello of Blood (1996)",
        "Apple Dumpling Gang, The (1975)",
        "Parent Trap, The (1961)",
        "William Shakespeare's Romeo and Juliet (1996)",
        "Transformers: The Movie, The (1986)",
        "Day the Earth Stood Still, The (1951)",
        "American Werewolf in London, An (1981)",
        "Amityville Horror, The (1979)",
        "Amityville Curse, The (1990)",
        "Birds, The (1963)",
        "Blob, The (1958)",
        "Body Snatcher, The (1945)",
        "Omen, The (1976)",
        "Jackie Chan's First Strike (1996)",
        "Free Willy 3: The Rescue (1997)",
        "Crossing Guard, The (1995)",
        "Like Water For Chocolate (Como agua para chocolate) (1992)",
        "Secret of Roan Inish, The (1994)",
        "Jungle Book, The (1994)",
        "Red Rock West (1992)",
        "Bronx Tale, A (1993)",
        "Dragonheart (1996)",
        "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1963)",
        "First Wives Club, The (1996)",
        "Philadelphia Story, The (1940)",
        "Apartment, The (1960)",
        "Maltese Falcon, The (1941)",
        "Adventures of Robin Hood, The (1938)",
        "Thin Man, The (1934)",
        "African Queen, The (1951)",
        "Candidate, The (1972)",
        "Streetcar Named Desire, A (1951)",
        "People vs. Larry Flynt, The (1996)",
        "My Left Foot (1989)",
        "Magnificent Seven, The (1954)",
        "Wings of Desire (1987)",
        "Third Man, The (1949)",
        "Boot, Das (1981)",
        "Treasure of the Sierra Madre, The (1948)",
        "Great Escape, The (1963)",
        "Deer Hunter, The (1978)",
        "Great Dictator, The (1940)",
        "Big Sleep, The (1946)",
        "Killing Fields, The (1984)",
        "My Life as a Dog (Mitt liv som hund) (1985)",
        "Man Who Would Be King, The (1975)",
        "Daytrippers, The (1996)",
        "Traveller (1997)",
        "Mouse Hunt (1997)",
        "Mis閞ables, Les (1995)",
        "Things to Do in Denver when You're Dead (1995)",
        "Young Poisoner's Handbook, The (1995)",
        "NeverEnding Story III, The (1994)",
        "Walk in the Clouds, A (1995)",
        "Farinelli: il castrato (1994)",
        "Interview with the Vampire (1994)",
        "Kid in King Arthur's Court, A (1995)",
        "Mary Shelley's Frankenstein (1994)",
        "Quick and the Dead, The (1995)",
        "Stephen King's The Langoliers (1995)",
        "Englishman Who Went Up a Hill, But Came Down a Mountain, The (1995)",
        "Piano, The (1993)",
        "Secret Garden, The (1993)",
        "Hour of the Pig, The (1993)",
        "Wild Bunch, The (1969)",
        "Fan, The (1996)",
        "Hunchback of Notre Dame, The (1996)",
        "Big Squeeze, The (1996)",
        "Police Story 4: Project S (Chao ji ji hua) (1993)",
        "Daniel Defoe's Robinson Crusoe (1996)",
        "American in Paris, An (1951)",
        "39 Steps, The (1935)",
        "Blue Angel, The (Blaue Engel, Der) (1930)",
        "Chamber, The (1996)",
        "Davy Crockett, King of the Wild Frontier (1955)",
        "Three Caballeros, The (1945)",
        "Sword in the Stone, The (1963)",
        "So Dear to My Heart (1949)",
        "Victor/Victoria (1982)",
        "Great Race, The (1965)",
        "Crying Game, The (1992)",
        "Christmas Carol, A (1938)",
        "Fog, The (1980)",
        "Howling, The (1981)",
        "Return of Martin Guerre, The (Retour de Martin Guerre, Le) (1982)",
        "Tin Drum, The (Blechtrommel, Die) (1979)",
        "Cook the Thief His Wife & Her Lover, The (1989)",
        "Grifters, The (1990)",
        "The Innocent (1994)",
        "Thin Blue Line, The (1988)",
        "Once Upon a Time in the West (1969)",
        "Quiet Man, The (1952)",
        "Seventh Seal, The (Sjunde inseglet, Det) (1957)",
        "Rosencrantz and Guildenstern Are Dead (1990)",
        "M (1931)",
        "Manchurian Candidate, The (1962)",
        "Alien 3 (1992)",
        "Blood For Dracula (Andy Warhol's Dracula) (1974)",
        "Blood Beach (1981)",
        "Bride of Frankenstein (1935)",
        "Nosferatu (Nosferatu, eine Symphonie des Grauens) (1922)",
        "Crucible, The (1996)",
        "Fire on the Mountain (1996)",
        "Conan the Barbarian (1981)",
        "Rocket Man (1997)",
        "Perfect World, A (1993)",
        "Jackal, The (1997)",
        "American President, The (1995)",
        "Persuasion (1995)",
        "Basketball Diaries, The (1995)",
        "Browning Version, The (1994)",
        "Wonderful, Horrible Life of Leni Riefenstahl, The (1993)",
        "House of the Spirits, The (1993)",
        "Bad Moon (1996)",
        "Substance of Fire, The (1996)",
        "Carrington (1995)",
        "Juror, The (1996)",
        "Canadian Bacon (1994)",
        "Queen Margot (Reine Margot, La) (1994)",
        "Last Supper, The (1995)",
        "Crow: City of Angels, The (1996)",
        "Ruling Class, The (1972)",
        "Saint, The (1997)",
        "MatchMaker, The (1997)",
        "Replacement Killers, The (1998)",
        "Burnt By the Sun (1994)",
        "Across the Sea of Time (1995)",
        "Addiction, The (1995)",
        "Mute Witness (1994)",
        "Prophecy, The (1995)",
        "Don Juan DeMarco (1995)",
        "Dumb & Dumber (1994)",
        "Little Odessa (1994)",
        "Beyond Bedlam (1993)",
        "Perez Family, The (1995)",
        "Swimming with Sharks (1995)",
        "Baby-Sitters Club, The (1995)",
        "Richie Rich (1994)",
        "Boys Life (1995)",
        "In the Mouth of Madness (1995)",
        "Air Up There, The (1994)",
        "Heaven & Earth (1993)",
        "Program, The (1993)",
        "Shadow, The (1994)",
        "Thirty-Two Short Films About Glenn Gould (1993)",
        "Celluloid Closet, The (1995)",
        "Great Day in Harlem, A (1994)",
        "Faces (1968)",
        "Great White Hype, The (1996)",
        "Arrival, The (1996)",
        "Phantom, The (1996)",
        "Power 98 (1995)",
        "Gay Divorcee, The (1934)",
        "In the Line of Duty 2 (1987)",
        "Loch Ness (1995)",
        "Glimmer Man, The (1996)",
        "Shaggy Dog, The (1959)",
        "Murder, My Sweet (1944)",
        "Perfect Candidate, A (1996)",
        "Two or Three Things I Know About Her (1966)",
        "Bloody Child, The (1996)",
        "Paris Was a Woman (1995)",
        "Believers, The (1987)",
        "Nosferatu a Venezia (1986)",
        "Garden of Finzi-Contini, The (Giardino dei Finzi-Contini, Il) (1970)",
        "Ice Storm, The (1997)",
        "Whole Wide World, The (1996)",
        "Hearts and Minds (1996)",
        "That Darn Cat! (1997)",
        "Peacemaker, The (1997)",
        "Telling Lies in America (1997)",
        "Life Less Ordinary, A (1997)",
        "One Night Stand (1997)",
        "Tango Lesson, The (1997)",
        "Sweet Hereafter, The (1997)",
        "Time Tracers (1995)",
        "Postman, The (1997)",
        "Winter Guest, The (1997)",
        "Big Lebowski, The (1998)",
        "Ma vie en rose (My Life in Pink) (1997)",
        "Oscar & Lucinda (1997)",
        "Vermin (1998)",
        "Nil By Mouth (1997)",
        "U.S. Marshalls (1998)",
        "City of Lost Children, The (1995)",
        "Two Bits (1995)",
        "Farewell My Concubine (1993)",
        "Raise the Red Lantern (1991)",
        "Flower of My Secret, The (Flor de mi secreto, La) (1995)",
        "Craft, The (1996)",
        "Island of Dr. Moreau, The (1996)",
        "Funeral, The (1996)",
        "Preacher's Wife, The (1996)",
        "Thousand Acres, A (1997)",
        "Smile Like Yours, A (1997)",
        "Killing Zoe (1994)",
        "Fox and the Hound, The (1981)",
        "Big Blue, The (Grand bleu, Le) (1988)",
        "Indian in the Cupboard, The (1995)",
        "Pushing Hands (1992)",
        "To Live (Huozhe) (1994)",
        "Orlando (1993)",
        "Some Folks Call It a Sling Blade (1993)",
        "Month by the Lake, A (1995)",
        "Affair to Remember, An (1957)",
        "Inspector General, The (1949)",
        "Grateful Dead (1995)",
        "Substitute, The (1996)",
        "Trigger Effect, The (1996)",
        "Rich Man's Wife, The (1996)",
        "Blood & Wine (1997)",
        "Underworld (1997)",
        "Beautician and the Beast, The (1997)",
        "Keys to Tulsa (1997)",
        "Last Time I Committed Suicide, The (1997)",
        "Big Green, The (1995)",
        "Stupids, The (1996)",
        "Pest, The (1997)",
        "That Darn Cat! (1997)",
        "Double vie de V閞onique, La (Double Life of Veronique, The) (1991)",
        "Until the End of the World (Bis ans Ende der Welt) (1991)",
        "Shiloh (1997)",
        "Tie Me Up! Tie Me Down! (1990)",
        "Die xue shuang xiong (Killer, The) (1989)",
        "8 1/2 (1963)",
        "Mrs. Dalloway (1997)",
        "Lay of the Land, The (1997)",
        "Shooter, The (1995)",
        "Beverly Hillbillies, The (1993)",
        "Quest, The (1996)",
        "Two if by Sea (1996)",
        "Paper, The (1994)",
        "Ghost and Mrs. Muir, The (1947)",
        "Associate, The (1996)",
        "Simple Twist of Fate, A (1994)",
        "Cronos (1992)",
        "Pallbearer, The (1996)",
        "War, The (1994)",
        "Adventures of Pinocchio, The (1996)",
        "Evening Star, The (1996)",
        "Four Days in September (1997)",
        "Little Princess, A (1995)",
        "Koyaanisqatsi (1983)",
        "Star Maker, The (Uomo delle stelle, L') (1995)",
        "Pyromaniac's Love Story, A (1995)",
        "Man of No Importance, A (1994)",
        "Pagemaster, The (1994)",
        "Celestial Clockwork (1994)",
        "Curdled (1996)",
        "Carried Away (1996)",
        "It's My Party (1995)",
        "Bloodsport 2 (1995)",
        "Thin Line Between Love and Hate, A (1996)",
        "Commandments (1997)",
        "Hate (Haine, La) (1995)",
        "Flirting With Disaster (1996)",
        "Red Firecracker, Green Firecracker (1994)",
        "Two Much (1996)",
        "C'est arriv?pr鑣 de chez vous (1992)",
        "Firestorm (1998)",
        "Newton Boys, The (1998)",
        "Feast of July (1995)",
        "Faithful (1996)",
        "Twelfth Night (1996)",
        "Mark of Zorro, The (1940)",
        "Surviving Picasso (1996)",
        "I'm Not Rappaport (1996)",
        "Umbrellas of Cherbourg, The (Parapluies de Cherbourg, Les) (1964)",
        "They Made Me a Criminal (1939)",
        "Last Time I Saw Paris, The (1954)",
        "Farewell to Arms, A (1932)",
        "Innocents, The (1961)",
        "Old Man and the Sea, The (1958)",
        "Truman Show, The (1998)",
        "Chungking Express (1994)",
        "Jupiter's Wife (1994)",
        "Doors, The (1991)",
        "Road to Wellville, The (1994)",
        "War Room, The (1993)",
        "Hard Eight (1996)",
        "Quiet Room, The (1996)",
        "Original Gangstas (1996)",
        "Backbeat (1993)",
        "Alphaville (1965)",
        "Rendezvous in Paris (Rendez-vous de Paris, Les) (1995)",
        "Cyclo (1995)",
        "Relic, The (1997)",
        "Fille seule, La (A Single Girl) (1995)",
        "Love! Valour! Compassion! (1997)",
        "Palookaville (1996)",
        "Phat Beach (1996)",
        "Portrait of a Lady, The (1996)",
        "Sum of Us, The (1994)",
        "Wild Reeds (1994)",
        "Women, The (1939)",
        "Caught (1996)",
        "Hugo Pool (1997)",
        "Welcome To Sarajevo (1997)",
        "Major Payne (1994)",
        "Low Down Dirty Shame, A (1994)",
        "Cowboy Way, The (1994)",
        "Endless Summer 2, The (1994)",
        "Inkwell, The (1994)",
        "Switchblade Sisters (1975)",
        "That Old Feeling (1997)",
        "Letter From Death Row, A (1998)",
        "Boys of St. Vincent, The (1993)",
        "Before the Rain (Pred dozhdot) (1994)",
        "Strawberry and Chocolate (Fresa y chocolate) (1993)",
        "Savage Nights (Nuits fauves, Les) (1992)",
        "Family Thing, A (1996)",
        "Purple Noon (1960)",
        "Cemetery Man (Dellamorte Dellamore) (1994)",
        "Kim (1950)",
        "Marlene Dietrich: Shadow and Light (1996)",
        "Maybe, Maybe Not (Bewegte Mann, Der) (1994)",
        "Secret Agent, The (1996)",
        "Guilty as Sin (1993)",
        "In the Realm of the Senses (Ai no corrida) (1976)",
        "Goofy Movie, A (1995)",
        "King of the Hill (1993)",
        "Scout, The (1994)",
        "Night Falls on Manhattan (1997)",
        "Awfully Big Adventure, An (1995)",
        "Poison Ivy II (1995)",
        "Ready to Wear (Pret-A-Porter) (1994)",
        "N閚ette et Boni (1996)",
        "Big Bang Theory, The (1994)",
        "Other Voices, Other Rooms (1997)",
        "Twisted (1996)",
        "Full Speed (1996)",
        "Ghost in the Shell (Kokaku kidotai) (1995)",
        "Van, The (1996)",
        "Old Lady Who Walked in the Sea, The (Vieille qui marchait dans la mer, La) (1991)",
        "Night Flier (1997)",
        "Blink (1994)",
        "A Chef in Love (1996)",
        "Contempt (M閜ris, Le) (1963)",
        "Tie That Binds, The (1995)",
        "Designated Mourner, The (1997)",
        "Designated Mourner, The (1997)",
        "Run of the Country, The (1995)",
        "Nothing to Lose (1994)",
        "Bread and Chocolate (Pane e cioccolata) (1973)",
        "Talking About Sex (1994)",
        "Robocop 3 (1993)",
        "Killer (Bulletproof Heart) (1994)",
        "Manny & Lo (1996)",
        "Grass Harp, The (1995)",
        "Shall We Dance? (1937)",
        "Jack and Sarah (1995)",
        "Country Life (1994)",
        "Simple Wish, A (1997)",
        "Star Kid (1997)",
        "Ayn Rand: A Sense of Life (1997)",
        "Kicked in the Head (1997)",
        "Band Wagon, The (1953)",
        "Late Bloomers (1996)",
        "Getaway, The (1994)",
        "New York Cop (1996)",
        "National Lampoon's Senior Trip (1995)",
        "Delta of Venus (1994)",
        "Carmen Miranda: Bananas Is My Business (1994)",
        "Babyfever (1994)",
        "Very Natural Thing, A (1974)",
        "Walk in the Sun, A (1945)",
        "Pompatus of Love, The (1996)",
        "Horse Whisperer, The (1998)",
        "Journey of August King, The (1995)",
        "Neon Bible, The (1995)",
        "Homage (1995)",
        "Open Season (1996)",
        "Metisse (Caf?au Lait) (1993)",
        "Wooden Man's Bride, The (Wu Kui) (1994)",
        "Loaded (1994)",
        "August (1996)",
        "Captives (1994)",
        "Of Love and Shadows (1994)",
        "Low Life, The (1994)",
        "An Unforgettable Summer (1994)",
        "Last Klezmer: Leopold Kozlowski, His Life and Music, The (1995)",
        "My Life and Times With Antonin Artaud (En compagnie d'Antonin Artaud) (1993)",
        "Midnight Dancers (Sibak) (1994)",
        "Two Deaths (1995)",
        "Stefano Quantestorie (1993)",
        "Crude Oasis, The (1995)",
        "Hedd Wyn (1992)",
        "Convent, The (Convento, O) (1995)",
        "Lotto Land (1995)",
        "Story of Xinghua, The (1993)",
        "Day the Sun Turned Cold, The (Tianguo niezi) (1994)",
        "Dingo (1992)",
        "Ballad of Narayama, The (Narayama Bushiko) (1958)",
        "Every Other Weekend (1990)",
        "Mille bolle blu (1993)",
        "Crows and Sparrows (1949)",
        "Lover's Knot (1996)",
        "Shadow of Angels (Schatten der Engel) (1976)",
        "1-900 (1994)",
        "Venice/Venice (1992)",
        "Ed's Next Move (1996)",
        "For the Moment (1994)",
        "The Deadly Cure (1996)",
        "Boys in Venice (1996)",
        "Sexual Life of the Belgians, The (1994)",
        "Search for One-eye Jimmy, The (1996)",
        "American Strays (1996)",
        "Leopard Son, The (1996)",
        "Bird of Prey (1996)",
        "Johnny 100 Pesos (1993)",
        "JLG/JLG - autoportrait de d閏embre (1994)",
        "Forbidden Christ, The (Cristo proibito, Il) (1950)",
        "I Can't Sleep (J'ai pas sommeil) (1994)",
        "Machine, The (1994)",
        "Stranger, The (1994)",
        "Good Morning (1971)",
        "Falling in Love Again (1980)",
        "Cement Garden, The (1993)",
        "Hotel de Love (1996)",
        "Rhyme & Reason (1997)",
        "Hollow Reed (1996)",
        "Losing Chase (1996)",
        "Bonheur, Le (1965)",
        "Second Jungle Book: Mowgli & Baloo, The (1997)",
        "Squeeze (1996)",
        "Roseanna's Grave (For Roseanna) (1997)",
        "Tetsuo II: Body Hammer (1992)",
        "Gabbeh (1996)",
        "Mondo (1996)",
        "Innocent Sleep, The (1995)",
        "For Ever Mozart (1996)",
        "Locusts, The (1997)",
        "Stag (1997)",
        "Hurricane Streets (1998)",
        "Stonewall (1995)",
        "Anna (1996)",
        "Picture Bride (1995)",
        "Ciao, Professore! (1993)",
        "Caro Diario (Dear Diary) (1994)",
        "Withnail and I (1987)",
        "Boy's Life 2 (1997)",
        "Specialist, The (1994)",
        "Gordy (1995)",
        "Swan Princess, The (1994)",
        "Harlem (1993)",
        "Land Before Time III: The Time of the Great Giving (1995) (V)",
        "Coldblooded (1995)",
        "Next Karate Kid, The (1994)",
        "Turning, The (1992)",
        "Joy Luck Club, The (1993)",
        "Gilligan's Island: The Movie (1998)",
        "My Crazy Life (Mi vida loca) (1993)",
        "Walking Dead, The (1995)",
        "SubUrbia (1997)",
        "Ill Gotten Gains (1997)",
        "Legal Deceit (1997)",
        "Mighty, The (1998)",
        "Men of Means (1998)",
        "Steal Big, Steal Little (1995)",
        "Mr. Jones (1993)",
        "Panther (1995)",
        "Moonlight and Valentino (1995)",
        "Scarlet Letter, The (1995)",
        "Bye Bye, Love (1995)",
        "Century (1993)",
        "My Favorite Season (1993)",
        "Golden Earrings (1947)",
        "Lady of Burlesque (1943)",
        "Angel on My Shoulder (1946)",
        "Angel and the Badman (1947)",
        "Outlaw, The (1943)",
        "Beat the Devil (1954)",
        "Love Is All There Is (1996)",
        "Damsel in Distress, A (1937)",
        "Madame Butterfly (1995)",
        "Sleepover (1995)",
        "Here Comes Cookie (1935)",
        "Thieves (Voleurs, Les) (1996)",
        "Boys, Les (1997)",
        "Stars Fell on Henrietta, The (1995)",
        "Last Summer in the Hamptons (1995)",
        "Margaret's Museum (1995)",
        "Saint of Fort Washington, The (1993)",
        "Cure, The (1995)",
        "Gumby: The Movie (1995)",
        "Visitors, The (Visiteurs, Les) (1993)",
        "Little Princess, The (1939)",
        "Raw Deal (1948)",
        "Gate of Heavenly Peace, The (1995)",
        "Man in the Iron Mask, The (1998)",
        "Jerky Boys, The (1994)",
        "Colonel Chabert, Le (1994)",
        "Girl in the Cadillac (1995)",
        "Fausto (1993)",
        "Tough and Deadly (1995)",
        "Window to Paris (1994)",
        "Modern Affair, A (1995)",
        "Mostro, Il (1994)",
        "Flirt (1995)",
        "Line King: Al Hirschfeld, The (1996)",
        "Farmer & Chase (1995)",
        "Grosse Fatigue (1994)",
        "Santa with Muscles (1996)",
        "Prisoner of the Mountains (Kavkazsky Plennik) (1996)",
        "Naked in New York (1994)",
        "Gold Diggers: The Secret of Bear Mountain (1995)",
        "Bewegte Mann, Der (1994)",
        "Killer: A Journal of Murder (1995)",
        "Three Lives and Only One Death (1996)",
        "Babysitter, The (1995)",
        "Mad Dog Time (1996)",
        "World of Apu, The (Apur Sansar) (1959)",
        "Sprung (1997)",
        "Dream With the Fishes (1997)",
        "Wings of Courage (1995)",
        "Wedding Gift, The (1994)",
        "Race the Sun (1996)",
        "Fear, The (1995)",
        "Trial by Jury (1994)",
        "Good Man in Africa, A (1994)",
        "Object of My Affection, The (1998)",
        "Far From Home: The Adventures of Yellow Dog (1995)",
        "Foreign Student (1994)",
        "I Don't Want to Talk About It (De eso no se habla) (1993)",
        "Twin Town (1997)",
        "Enfer, L' (1994)",
        "Aiqing wansui (1994)",
        "Cosi (1996)",
        "All Over Me (1997)",
        "Being Human (1993)",
        "Amazing Panda Adventure, The (1995)",
        "Beans of Egypt, Maine, The (1994)",
        "Scarlet Letter, The (1926)",
        "Johns (1996)",
        "Frankie Starlight (1995)",
        "Shadows (Cienie) (1988)",
        "Show, The (1995)",
        "The Courtyard (1995)",
        "Dream Man (1995)",
        "Glass Shield, The (1994)",
        "Hunted, The (1995)",
        "Underneath, The (1995)",
        "Safe Passage (1994)",
        "Secret Adventures of Tom Thumb, The (1993)",
        "Condition Red (1995)",
        "Yankee Zulu (1994)",
        "Hostile Intentions (1994)",
        "Clean Slate (Coup de Torchon) (1981)",
        "Tigrero: A Film That Was Never Made (1994)",
        "Eye of Vichy, The (Oeil de Vichy, L') (1993)",
        "Promise, The (Versprechen, Das) (1994)",
        "To Cross the Rubicon (1991)",
        "Daens (1992)",
        "Man from Down Under, The (1943)",
        "Careful (1992)",
        "Vermont Is For Lovers (1992)",
        "Vie est belle, La (Life is Rosey) (1987)",
        "Quartier Mozart (1992)",
        "Touki Bouki (Journey of the Hyena) (1973)",
        "Wend Kuuni (God's Gift) (1982)",
        "Spirits of the Dead (Tre passi nel delirio) (1968)",
        "Pharaoh's Army (1995)",
        "I, Worst of All (Yo, la peor de todas) (1990)",
        "Hungarian Fairy Tale, A (1987)",
        "Death in the Garden (Mort en ce jardin, La) (1956)",
        "Collectionneuse, La (1967)",
        "Baton Rouge (1988)",
        "Liebelei (1933)",
        "Woman in Question, The (1950)",
        "T-Men (1947)",
        "Invitation, The (Zaproszenie) (1986)",
        "Symphonie pastorale, La (1946)",
        "American Dream (1990)",
        "Lashou shentan (1992)",
        "Terror in a Texas Town (1958)",
        "Salut cousin! (1996)",
        "To Have, or Not (1995)",
        "Duoluo tianshi (1995)",
        "Magic Hour, The (1998)",
        "Death in Brunswick (1991)",
        "Shopping (1994)",
        "Nemesis 2: Nebula (1995)",
        "City of Industry (1997)",
        "Someone Else's America (1995)",
        "Guantanamera (1994)",
        "Office Killer (1997)",
        "Price Above Rubies, A (1998)",
        "Angela (1995)",
        "He Walked by Night (1948)",
        "Hurricane Streets (1998)",
        "Truth or Consequences, N.M. (1997)",
        "Intimate Relations (1996)",
        "Leading Man, The (1996)",
        "Tokyo Fist (1995)",
        "Reluctant Debutante, The (1958)",
        "Warriors of Virtue (1997)",
        "Desert Winds (1995)",
        "Hugo Pool (1997)",
        "All Things Fair (1996)",
        "Sixth Man, The (1997)",
        "Butterfly Kiss (1995)",
        "Paris, France (1993)",
        # "C閞閙onie, La (1995)",  # 错误数据
        "Nobody Loves Me (Keiner liebt mich) (1994)",
        "Wife, The (1995)",
        "Silence of the Palace, The (Saimt el Qusur) (1994)",
        "Slingshot, The (1993)",
        "Land and Freedom (Tierra y libertad) (1995)",
        # "?k鰈dum klaka (Cold Fever) (1994)",  # 错误数据
        "Etz Hadomim Tafus (Under the Domin Tree) (1994)",
        "Two Friends (1986)",
        "Brothers in Trouble (1995)",
        "Girls Town (1996)",
        "Bitter Sugar (Azucar Amargo) (1996)",
        "Eighth Day, The (1996)",
        "Dadetown (1995)",
        "Sudden Manhattan (1996)",
        "Butcher Boy, The (1998)",
        "Men With Guns (1997)",
        "Niagara, Niagara (1997)",
        "Big One, The (1997)",
        "Butcher Boy, The (1998)",
        "Spanish Prisoner, The (1997)",
        "Temptress Moon (Feng Yue) (1996)",
        "Favor, The (1994)",
        "Little City (1998)",
        "Target (1995)",
        "Substance of Fire, The (1996)",
        "Getting Away With Murder (1996)",
        "Small Faces (1995)",
        "New Age, The (1994)",
        "Brother's Kiss, A (1997)",
        "Ripe (1996)",
        "Next Step, The (1995)",
        "Wedding Bell Blues (1996)",
        "MURDER and murder (1996)",
        "Tainted (1998)",
        "Further Gesture, A (1996)",
        "Mirage (1995)",
        "Mamma Roma (1962)",
        "Sunchaser, The (1996)",
        "War at Home, The (1996)",
        "Sweet Nothing (1995)",
        "Mat' i syn (1997)",
        "You So Crazy (1994)",
        "Scream of Stone (Schrei aus Stein) (1991)",
    ]

    # 准备CSV
    header = []
    csv_file = open('imdb.csv', 'a')
    csv_write = csv.writer(csv_file, dialect='excel')

    for title in title_list:
        imdb_id = get_imdb_id(title)
        if not imdb_id:
            print('movie not found: %s' % title)
            continue
        imdb_info = get_imdb_info(imdb_id)
        imdb_info['title'] = title  # 原始标题

        # 写入CSV
        if not header:
            header = imdb_info.keys()
            csv_write.writerow(header)
        csv_write.writerow(imdb_info.values())
    csv_file.close()


if __name__ == '__main__':
    # test_title = 'William Shakespeare\'s Romeo and Juliet (1996)'
    # test_imdb_id = get_imdb_id(test_title)
    # get_imdb_info(test_imdb_id)
    # get_imdb_info('tt0117509')
    run()
