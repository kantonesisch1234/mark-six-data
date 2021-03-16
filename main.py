import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json

def scrape_mark_six_history(year_range):
    base_url = 'http://lottery.hk/liuhecai/jieguo/'
    lottery_date = []
    lottery_no = []
    
    for year in range(year_range[1],year_range[0]-1,-1):
    
        url = base_url + str(year)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lottery_date += [tag.get_text() for tag in soup.find('body').find_all('td')[0::4]]
        lottery_no += [tuple([int(tag2.get_text()) for tag2 in tag.find_all('li')]) for tag in soup.find('body').find_all('td')[2::4]]
        
    lottery_dict = dict(zip(lottery_date, lottery_no))
    
    return lottery_dict

def combine_lottery_no(lottery_dict):
    combined_lottery_no = []
    for lottery_no in lottery_dict.values():
        combined_lottery_no += list(lottery_no)
    return sorted(combined_lottery_no)

def get_freq_dict(lottery_dict):
    combined_lottery_no_sorted = combine_lottery_no(lottery_dict)
    freq_dict = dict()
    for num in range(1,50):
        freq_dict[num] = 0
    freq_dict_keys = list(range(1,50))
    for num in combined_lottery_no_sorted:
        freq_dict[num] += 1
    return freq_dict
    
def sort_lottery_dict_by_freq(lottery_dict):
    freq_dict = get_freq_dict(lottery_dict)
    sorted_keys = sorted(freq_dict, key=freq_dict.get)[::-1]
    for key in sorted_keys:
        print(str(key) + ': ' + str(freq_dict[key]))
    
def plot_freq(lottery_dict):
    freq_dict = get_freq_dict(lottery_dict)
    plt.figure(num=None, figsize=(15,6), dpi=80)
    plt.bar(range(1,50), list(freq_dict.values()), width=0.8, tick_label=range(1,50))
    plt.show()
    
def save_to_json(lottery_dict):
    with open('data.json', 'w') as outfile:
        json.dump(lottery_dict, outfile)
        
def read_from_json():
    with open('data.txt') as json_file:
        data = json.load(json_file)
    return data
  
if __name__ == '__main__':
    lottery_dict = scrape_mark_six_history((1993,2021))
    save_to_json(lottery_dict)
    plot_freq(lottery_dict)
    sort_lottery_dict_by_freq(lottery_dict)
