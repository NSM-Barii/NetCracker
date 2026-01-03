# Evil Twin Captive Portals

Captive portal templates for ethical penetration testing.

## Portal List

| # | Name | SSID | Target | Data Captured |
|---|------|------|--------|---------------|
| 1 | LA Fitness | LA Fitness | Gym members | Email, Phone |
| 2 | Starbucks | Starbucks WiFi | Coffee customers | Email, Name |
| 3 | Airport | Airport_Free_WiFi | Travelers | Email, Flight# |
| 4 | Marriott | Marriott_Guest | Hotel guests | Room#, Last Name |
| 5 | Subway | SUBWAY_Free_WiFi | Fast food customers | Email |
| 6 | McDonald's | McDonalds_Free_WiFi | Fast food customers | Email |
| 7 | Target | Target Guest WiFi | Retail customers | Email, Zip Code |
| 8 | Walmart | Walmart WiFi | Retail customers | Email |
| 9 | Hospital | Hospital_Guest | Visitors/Patients | Name, Phone |
| 10 | Library | Public_Library_WiFi | Library visitors | Library Card# |
| 11 | University | Campus_WiFi | Students | Student ID, Email |
| 12 | Panera | Panera WiFi | Cafe customers | Email |
| 13 | Best Buy | BestBuy_Guest | Electronics customers | Email |
| 14 | Corporate | CORP_Guest_WiFi | Office visitors | Name, Company |
| 15 | Hilton | Hilton_Honors | Hotel guests | Room#, Last Name |
| 16 | Delta | Delta Sky Club | Airline passengers | SkyMiles#, Email |
| 17 | Apple Store | Apple Store | Tech customers | Apple ID |
| 18 | YMCA | YMCA_Member_WiFi | Gym members | Member ID |
| 19 | Whole Foods | Whole_Foods_WiFi | Grocery customers | Email |
| 20 | CVS | CVS WiFi | Pharmacy customers | Phone Number |

## Usage
1. Select portal number in Evil Twin module
2. SSID automatically set
3. Credentials logged to console/file

## Ethical Use Only
- Authorized pentesting only
- Written permission required
- Secure credential handling
- Delete data after testing

## Adding Portals
1. Create `portal_X/` directory
2. Add `index.html`, `success.html`
3. Update `nsm_deauth.py` dictionary
4. Update this README
