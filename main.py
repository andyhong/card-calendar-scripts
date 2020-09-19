import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import time
import os

from discord import send_new_set, update_set

client = MongoClient(os.environ["MONGO_URI"])
db = client["tempest"]
col = db["cards"]

def download_card_sets():

  options = webdriver.ChromeOptions()
  options.add_argument("headless")
  driver = webdriver.Chrome(options=options)
  driver.get("https://blowoutforums.com/showthread.php?t=803")
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  post = soup.find("div", id="post_message_4305")
  category_nodes = post.find_all("u")

  card_sets = []
  for cat in category_nodes:
    next_sib = cat.next_sibling
    while next_sib.name != "u" and next_sib is not None:
      while next_sib.name == "br" and next_sib is not None:
        next_sib = next_sib.next_sibling
      if next_sib.strip() != "":
        if len(next_sib.strip().split(" ", 1)[0]) == 8 and "/" not in next_sib.strip().split(" ", 1):
          release_date = next_sib.strip().split(" ", 1)[0]
          name = next_sib.strip().split(" ", 1)[1].strip()
        else:
          release_date = "TBD"
          if "TBD" not in next_sib.strip().split(" ", 2)[2]:
            name = next_sib.strip().split(" ", 2)[2]
          else:
            name = next_sib.strip().split("TBD", 1)[1].strip()
        card_set = {
          "name": name,
          "release_date": release_date,
          "category": cat.text.strip().strip(":").lower().replace(" ", "_"),
        }
        card_sets.append(card_set)
      next_sib = next_sib.next_sibling
      if next_sib is None:
        break
  return card_sets

def check_for_updates(card_sets):

  new_sets = []
  updated_sets = []

  for s in card_sets:
    q = col.find_one({"name": s["name"], "category": s["category"]})
    if q is None:
      insert = col.insert_one(s)
      if insert.inserted_id:
        print(f"Added {s['name']} @ _id {insert.inserted_id}")
        new_sets.append(s)
    else:
      if q["release_date"] != s["release_date"]:
        update = col.update_one({"_id": q["_id"]}, {"$set": {"release_date": s["release_date"]}})
        if update.modified_count == 1:
          print(f"Updated release date for {s['name']} @ _id {q['_id']} ({s['release_date']})")
          updated_sets.append(s)
  return new_sets, updated_sets

def send_to_discord(new, updates):
  webhook = "https://discord.com/api/webhooks/743242754313945098/xPfU3c8HfSQ2pqMxDdi3a0tJOEomUZbLCAzKlYxbWBl4MFLdD6XGwLjj9j-CNiAzzYZL"
  for n in new:
    send_new_set(webhook, n)
    time.sleep(1)
  for u in updates:
    update_set(webhook, u)
    time.sleep(1)

if __name__ == "__main__":

  card_sets = download_card_sets()
  new, updates = check_for_updates(card_sets)

  if len(new) > 0 or len(updates) > 0:
    send_to_discord(new, updates)
  else:
    print("No updates found. Exiting.")
