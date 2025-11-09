# County Shelter Access Portal (CSAP)

## Introduction

Natural disasters such as hurricanes, floods, and wildfires displace thousands of people every year, leaving them searching for safe shelter, food, and medical care. During these emergencies, many affected individuals struggle to locate available shelters or to know which ones have space, supplies or meet their specific needs (e.g. medical, pet-friendly).

---

## The Solution

Our solution is a Python-based web application that allows users to input their specific needs (such as food, water, medical aid and pet-friendliness). The user will be able to view nearby shelters along with their vacancy levels and details. The results are ranked recommendations based on proximity and fulfillment of needs. Users can then get directions to the selected shelter via Google Maps. Our prototype aims to show how quick data access can improve disaster response efficiency and guarantee as many people can find shelter as possible.

This application is intended to be used by individuals or families that are seeking shelter during hurricanes, floods, or wildfires. It may be able to additionally aid with emergency responders coordinating safe zones and resource allocation.

---

## Assumptions

Our application assumes that users have access to a smartphone or a computer with internet connectivity, shelter data is maintained and periodically updated by authorities or shelters and that GPS access is granted for accurate location detection. The current limitations of our application is that it requires internet access and can not be accessed offline.

Our prototype focuses on Pinellas County shelters in Florida as a sample area due to its frequent hurricane threats and established network of emergency shelters. However, this system is scalable to any region with publicly available shelter data. Our scope is focused on disaster preparedness and immediate response, not long-term recovery.

---

## How To Run

1. Download the repository and open the python files in your preferred IDE.
2. Install the required packages: `streamlit`, `folium`, `streamlit_folium`, `streamlit_geolocation`
3. Open your terminal in your IDE and type `streamlit run miniProduct.py` or type `python -m streamlit run miniProduct.py` if the first command doesn't work.
4. The `streamlit` app should open in your browser!

