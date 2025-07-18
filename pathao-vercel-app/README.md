# Pathao Delivery Order Creator

A smart web application for creating Pathao delivery orders with AI-powered parsing capabilities.

## Features

- **Smart Parsing**: Automatically extracts customer information from any text format
- **Auto-refresh**: Form clears automatically after successful order creation
- **Multiple Store Support**: Support for multiple Pathao merchant stores
- **Real-time Results**: Instant feedback with order details and tracking information

## Deployment to Vercel

### Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed globally: `npm install -g vercel`
3. Git repository (optional but recommended)

### Quick Deployment

#### Method 1: Using Vercel CLI

1. **Clone or download this project**
   ```bash
   # If you have the files locally
   cd pathao-vercel-app
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - What's your project's name? `pathao-delivery-creator`
   - In which directory is your code located? `./`

#### Method 2: Using Vercel Dashboard

1. **Push to GitHub** (recommended)
   - Create a new repository on GitHub
   - Push all files to the repository

2. **Import to Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Configure project settings (usually auto-detected)
   - Click "Deploy"

#### Method 3: Drag and Drop

1. **Zip the project folder**
   - Select all files in the `pathao-vercel-app` directory
   - Create a ZIP file

2. **Upload to Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Drag and drop your ZIP file
   - Click "Deploy"

### Configuration

The application is pre-configured with:
- **Client ID**: `K9b6W8VdEv`
- **Client Secret**: `wszrap3tCaVOba5DFcZu8AHrFgKtsZkOKvWxzFvD`
- **Username**: `iftekharm802@gmail.com`
- **Password**: `Ulalinux.12`

### Available Stores

- Sparkling arts and crafts (32411)
- Fashmecca (45099)
- Ki chai 2.0 (54186)
- Fashion Pallate BD (32410)
- Fashion pallate BD (97625) - Default

### File Structure

```
pathao-vercel-app/
├── index.html              # Main frontend application
├── api/
│   └── delivery.py         # Serverless function for Pathao API
├── vercel.json             # Vercel configuration
├── requirements.txt        # Python dependencies
├── package.json            # Project metadata
└── README.md              # This file
```

### Environment Variables (Optional)

For better security, you can set environment variables in Vercel:

1. Go to your project dashboard on Vercel
2. Navigate to Settings → Environment Variables
3. Add the following variables:
   - `PATHAO_CLIENT_ID`
   - `PATHAO_CLIENT_SECRET`
   - `PATHAO_USERNAME`
   - `PATHAO_PASSWORD`

Then update the `api/delivery.py` file to use these variables:

```python
import os

CLIENT_ID = os.environ.get('PATHAO_CLIENT_ID', 'K9b6W8VdEv')
CLIENT_SECRET = os.environ.get('PATHAO_CLIENT_SECRET', 'wszrap3tCaVOba5DFcZu8AHrFgKtsZkOKvWxzFvD')
USERNAME = os.environ.get('PATHAO_USERNAME', 'iftekharm802@gmail.com')
PASSWORD = os.environ.get('PATHAO_PASSWORD', 'Ulalinux.12')
```

### Usage

1. **Visit your deployed URL**
2. **Paste customer information** in any format, for example:
   ```
   Ahmed Rahman
   01712345678
   House 10, Road 5, Gulshan, Dhaka
   500 taka
   T-shirt and jeans
   Call before delivery
   ```
3. **Select the appropriate store**
4. **Click "Create Delivery Order"**
5. **View results** and wait for auto-refresh

### Supported Input Formats

The smart parser can handle various formats:

- **Structured format** with labels (Name:, Phone:, etc.)
- **Unstructured text** with information in any order
- **Mixed formats** with different separators
- **Bengali and English** text combinations

### Troubleshooting

#### Common Issues

1. **API Errors**: Check if Pathao credentials are correct
2. **CORS Issues**: Ensure the serverless function includes proper CORS headers
3. **Parsing Errors**: Verify that customer information includes name, phone, and address

#### Logs

View function logs in Vercel dashboard:
1. Go to your project dashboard
2. Click on "Functions" tab
3. Click on the function name to view logs

### Support

For issues or questions:
1. Check the Vercel deployment logs
2. Verify Pathao API credentials
3. Ensure all required files are included in deployment

### License

MIT License - feel free to modify and use for your projects.

