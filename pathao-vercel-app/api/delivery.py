import json
import re
import requests
import time
from http.server import BaseHTTPRequestHandler

# Pathao API Configuration
CLIENT_ID = 'K9b6W8VdEv'
CLIENT_SECRET = 'wszrap3tCaVOba5DFcZu8AHrFgKtsZkOKvWxzFvD'
USERNAME = 'iftekharm802@gmail.com'
PASSWORD = 'Ulalinux.12'
BASE_URL = 'https://api-hermes.pathao.com'

def get_access_token():
    """Get access token from Pathao API"""
    url = f'{BASE_URL}/aladdin/api/v1/issue-token'
    headers = {'Content-Type': 'application/json'}
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        raise Exception(f'Failed to get access token: {str(e)}')

def parse_customer_data(customer_data):
    """Advanced parsing of customer information from text input with AI-like intelligence"""
    parsed_data = {}
    text = customer_data.strip()
    
    # Enhanced patterns for different fields with multiple variations
    patterns = {
        'name': [
            r'(?:name|customer|recipient|client|person):\s*(.+?)(?:\n|$)',
            r'(?:^|\n)([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:\n|$)',  # Full name pattern
            r'(?:^|\n)name\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(?:^|\n)(.+?)\s*(?:phone|mobile|contact|address)',  # Name before phone/address
        ],
        'phone': [
            r'(?:phone|mobile|contact|number|tel|call):\s*(.+?)(?:\n|$)',
            r'(?:^|\n)(01[0-9]{9})\s*(?:\n|$)',  # Bangladesh mobile pattern
            r'(?:^|\n)(\+88\s*01[0-9]{9})\s*(?:\n|$)',  # With country code
            r'(?:^|\n)(01[0-9]{1}-[0-9]{4}-[0-9]{4})\s*(?:\n|$)',  # Formatted
            r'(?:^|\n)phone\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(\b01[0-9]{9}\b)',  # Any 11-digit number starting with 01
        ],
        'address': [
            r'(?:address|location|addr|delivery\s*address):\s*(.+?)(?:\n|$)',
            r'(?:house|flat|apartment|apt|building|road|street|area|sector|block)\s*[#\-:=]?\s*(.+?)(?:\n|$)',
            r'(?:^|\n)address\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(?:deliver\s*to|send\s*to|ship\s*to):\s*(.+?)(?:\n|$)',
        ],
        'amount': [
            r'(?:amount|price|cost|total|cod|cash|payment|tk|taka|৳):\s*(.+?)(?:\n|$)',
            r'(?:^|\n)(?:tk|taka|৳)\s*([0-9,]+)\s*(?:\n|$)',
            r'(?:^|\n)([0-9,]+)\s*(?:tk|taka|৳)\s*(?:\n|$)',
            r'(?:^|\n)amount\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(\b[0-9,]+\b)(?=\s*(?:tk|taka|৳|only))',  # Number followed by currency
        ],
        'description': [
            r'(?:description|item|product|details|goods|order):\s*(.+?)(?:\n|$)',
            r'(?:^|\n)description\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(?:what|item\s*details|product\s*name):\s*(.+?)(?:\n|$)',
        ],
        'instructions': [
            r'(?:instruction|note|special|comment|remark|message):\s*(.+?)(?:\n|$)',
            r'(?:^|\n)(?:special\s*)?instruction\s*[-:=]\s*(.+?)(?:\n|$)',
            r'(?:please|kindly|note|important):\s*(.+?)(?:\n|$)',
        ]
    }
    
    # Try each pattern for each field
    for field, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match and field not in parsed_data:
                value = match.group(1).strip()
                if value and len(value) > 1:  # Ensure meaningful content
                    parsed_data[field] = value
                    break
    
    # Smart fallback parsing - analyze the entire text structure
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # If we don't have a name, try to find it from the first meaningful line
    if 'name' not in parsed_data and lines:
        for line in lines:
            # Look for a line that looks like a name (2-3 words, proper case)
            name_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})$', line.strip())
            if name_match:
                parsed_data['name'] = name_match.group(1)
                break
    
    # If we don't have a phone, look for any 11-digit number starting with 01
    if 'phone' not in parsed_data:
        phone_match = re.search(r'\b(01[0-9]{9})\b', text)
        if phone_match:
            parsed_data['phone'] = phone_match.group(1)
    
    # If we don't have an address, look for lines with location indicators
    if 'address' not in parsed_data:
        for line in lines:
            if any(word in line.lower() for word in ['house', 'road', 'street', 'area', 'dhaka', 'chittagong', 'sylhet', 'khulna', 'rajshahi', 'barisal', 'rangpur', 'mymensingh']):
                parsed_data['address'] = line
                break
    
    # If we don't have an amount, look for any number that could be a price
    if 'amount' not in parsed_data:
        amount_match = re.search(r'\b([0-9,]{2,})\b', text)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            if amount_str.isdigit() and int(amount_str) > 10:  # Reasonable amount
                parsed_data['amount'] = int(amount_str)
    
    # Clean up phone number (remove non-digits except +)
    if 'phone' in parsed_data:
        phone = re.sub(r'[^\d+]', '', parsed_data['phone'])
        if phone.startswith('88'):
            phone = phone[2:]  # Remove country code
        if not phone.startswith('01') and len(phone) >= 10:
            phone = '01' + phone[-10:]  # Ensure proper format
        parsed_data['phone'] = phone
    
    # Clean up amount (extract numbers only)
    if 'amount' in parsed_data and isinstance(parsed_data['amount'], str):
        amount_match = re.search(r'([0-9,]+)', parsed_data['amount'])
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            parsed_data['amount'] = int(amount_str) if amount_str.isdigit() else 0
        else:
            parsed_data['amount'] = 0
    
    # Ensure amount is an integer
    if 'amount' not in parsed_data:
        parsed_data['amount'] = 0
    
    return parsed_data

def create_pathao_order(access_token, store_id, customer_data):
    """Create order via Pathao API"""
    url = f'{BASE_URL}/aladdin/api/v1/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Generate unique merchant order ID
    merchant_order_id = f'WEB_{int(time.time())}'
    
    # Prepare order data
    order_data = {
        'store_id': store_id,
        'merchant_order_id': merchant_order_id,
        'recipient_name': customer_data.get('name', 'Customer'),
        'recipient_phone': customer_data.get('phone', '01700000000'),
        'recipient_address': customer_data.get('address', 'Dhaka, Bangladesh'),
        'recipient_city': 1,  # Dhaka City ID
        'recipient_zone': 4,  # Default zone
        'recipient_area': 105,  # Default area
        'delivery_type': 48,  # Standard Delivery (48 hours)
        'item_type': 2,  # General Parcel
        'special_instruction': customer_data.get('instructions', 'Handle with care'),
        'item_quantity': 1,
        'item_weight': '0.5',
        'item_description': customer_data.get('description', 'General item'),
        'amount_to_collect': customer_data.get('amount', 0)
    }
    
    try:
        response = requests.post(url, headers=headers, json=order_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if e.response:
            error_data = e.response.text
            raise Exception(f'Pathao API error: {error_data}')
        else:
            raise Exception(f'Failed to create order: {str(e)}')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            customer_data_text = data.get('customer_data', '')
            store_id = data.get('store_id', 97625)  # Default to last store
            
            if not customer_data_text:
                self.send_error_response({'error': 'Customer data is required'}, 400)
                return
            
            # Parse customer data with enhanced parsing
            parsed_data = parse_customer_data(customer_data_text)
            
            # Validate required fields
            if not parsed_data.get('name'):
                self.send_error_response({'error': 'Customer name could not be found. Please include the customer name in your input.'}, 400)
                return
            if not parsed_data.get('phone'):
                self.send_error_response({'error': 'Customer phone number could not be found. Please include a valid phone number.'}, 400)
                return
            if not parsed_data.get('address'):
                self.send_error_response({'error': 'Customer address could not be found. Please include the delivery address.'}, 400)
                return
            
            # Get access token
            access_token = get_access_token()
            
            # Create order
            order_result = create_pathao_order(access_token, store_id, parsed_data)
            
            response_data = {
                'success': True,
                'message': 'Order created successfully',
                'parsed_data': parsed_data,
                'data': order_result.get('data', order_result)
            }
            
            self.send_success_response(response_data)
            
        except Exception as e:
            self.send_error_response({'success': False, 'error': str(e)}, 500)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, data, status_code):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

