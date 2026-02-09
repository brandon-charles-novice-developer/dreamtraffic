#!/bin/bash
set -e

echo "🚀 DreamTraffic Deployment Script"
echo "=================================="
echo ""

if [ -z "$VITE_SUPABASE_URL" ] || [ -z "$VITE_SUPABASE_ANON_KEY" ]; then
    echo "❌ Error: Missing Supabase environment variables"
    echo "Please set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY"
    exit 1
fi

echo "✅ Environment variables configured"
echo ""

echo "📦 Building frontend..."
cd prototype
npm install
npm run build

echo "✅ Frontend built successfully"
echo ""
echo "📁 Build output: prototype/dist/"
echo ""

echo "🎉 Deployment ready!"
echo ""
echo "Next steps:"
echo "  1. Deploy to Vercel: cd prototype && vercel --prod"
echo "  2. Deploy to Netlify: cd prototype && netlify deploy --prod"
echo "  3. Or serve locally: cd prototype && npm run preview"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
