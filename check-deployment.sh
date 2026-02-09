#!/bin/bash

echo "🔍 DreamTraffic Deployment Status Check"
echo "========================================"
echo ""

check_env_var() {
    if [ -z "${!1}" ]; then
        echo "❌ $1 is not set"
        return 1
    else
        echo "✅ $1 is set"
        return 0
    fi
}

all_good=0

echo "Environment Variables:"
check_env_var "VITE_SUPABASE_URL" || all_good=1
check_env_var "VITE_SUPABASE_ANON_KEY" || all_good=1
echo ""

if [ -d "prototype/dist" ]; then
    echo "✅ Frontend build exists (prototype/dist/)"
    echo "   Size: $(du -sh prototype/dist | cut -f1)"
else
    echo "❌ Frontend not built (run: cd prototype && npm run build)"
    all_good=1
fi
echo ""

if [ -f "prototype/dist/index.html" ]; then
    echo "✅ Frontend entry point exists"
else
    echo "❌ Frontend entry point missing"
    all_good=1
fi
echo ""

if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile present"
else
    echo "❌ Dockerfile missing"
    all_good=1
fi
echo ""

if [ -f "prototype/vercel.json" ]; then
    echo "✅ Vercel config present"
else
    echo "⚠️  Vercel config missing"
fi

if [ -f "prototype/netlify.toml" ]; then
    echo "✅ Netlify config present"
else
    echo "⚠️  Netlify config missing"
fi
echo ""

if [ $all_good -eq 0 ]; then
    echo "🎉 All checks passed! Ready to deploy."
    echo ""
    echo "Deploy with:"
    echo "  • Vercel: cd prototype && vercel --prod"
    echo "  • Netlify: cd prototype && netlify deploy --prod"
    exit 0
else
    echo "❌ Some checks failed. Please fix the issues above."
    exit 1
fi
