#!/bin/bash

echo "🚀 Pathao Delivery Creator - Vercel Deployment Script"
echo "=================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Checking Vercel authentication..."
vercel whoami || vercel login

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "📱 Your Pathao Delivery Creator is now live!"
echo ""
echo "🔗 Visit your deployment URL to start creating delivery orders."
echo "📖 Check the README.md for usage instructions."

