# DreamTraffic Deployment Guide

## Pre-Deployment Checklist

- [x] Supabase database setup complete
- [x] Database schema migrated with RLS policies
- [x] Reference data seeded (11 supply paths, 8 DSP specs)
- [x] Frontend built successfully
- [x] Environment variables configured
- [x] Deployment configurations created

## Architecture Overview

```
┌─────────────────┐
│  React Frontend │  (Vite SPA)
│  Static Hosting │  → Vercel/Netlify
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│    Supabase     │  (PostgreSQL + RLS)
│    Database     │  https://zomhbocysksmtaqulckv.supabase.co
└────────▲────────┘
         │
         │ PostgreSQL Protocol
         │
┌────────┴────────┐
│  Python Backend │  (CLI + Agents)
│  Local/Docker   │  Claude Agent SDK
└─────────────────┘
```

## Current Status

✅ **Database**: Deployed and configured on Supabase
- URL: https://zomhbocysksmtaqulckv.supabase.co
- Tables: 6 tables with RLS enabled
- Reference data: Fully seeded

✅ **Frontend**: Production-ready build
- Location: `prototype/dist/`
- Size: ~246 KB (gzipped: ~72 KB)
- Framework: React 19 + Vite 6

✅ **Backend**: CLI application ready
- Framework: Claude Agent SDK
- Python: 3.12+
- Package manager: uv

## Deployment Options

### Option 1: Frontend on Vercel (Recommended)

**Why Vercel:**
- Zero-config Vite support
- Automatic SSL
- Global CDN
- Preview deployments for PRs

**Steps:**

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy frontend:
```bash
cd prototype
vercel --prod
```

3. Set environment variables in Vercel dashboard:
```
VITE_SUPABASE_URL=https://zomhbocysksmtaqulckv.supabase.co
VITE_SUPABASE_ANON_KEY=<from .env file>
```

4. Access your deployed app at: `https://dreamtraffic-prototype.vercel.app`

### Option 2: Frontend on Netlify

**Why Netlify:**
- Simple drag-and-drop deploy
- Form handling
- Serverless functions support

**Steps:**

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Deploy frontend:
```bash
cd prototype
netlify deploy --prod
```

3. Set environment variables in Netlify dashboard:
```
VITE_SUPABASE_URL=https://zomhbocysksmtaqulckv.supabase.co
VITE_SUPABASE_ANON_KEY=<from .env file>
```

### Option 3: Self-Hosted with Docker

**For complete control:**

1. Build Docker image:
```bash
docker build -t dreamtraffic:latest .
```

2. Run backend container:
```bash
docker run -d \
  -e LUMAAI_API_KEY=<your-key> \
  -e ANTHROPIC_API_KEY=<your-key> \
  -e VITE_SUPABASE_URL=https://zomhbocysksmtaqulckv.supabase.co \
  -e VITE_SUPABASE_ANON_KEY=<your-key> \
  dreamtraffic:latest
```

3. Serve frontend with nginx/Apache:
```bash
cp -r prototype/dist/* /var/www/html/
```

## Environment Variables

### Required for Frontend
```env
VITE_SUPABASE_URL=https://zomhbocysksmtaqulckv.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Required for Backend
```env
LUMAAI_API_KEY=luma-xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
VITE_SUPABASE_URL=https://zomhbocysksmtaqulckv.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Post-Deployment Verification

### 1. Test Database Connection

```bash
curl -X POST 'https://zomhbocysksmtaqulckv.supabase.co/rest/v1/campaigns' \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"select": "*"}'
```

Expected: JSON response with campaign data (may be empty array)

### 2. Test Frontend

Open deployed URL and verify:
- [ ] Page loads without errors
- [ ] Supabase client initializes (check browser console)
- [ ] No CORS errors
- [ ] Navigation works
- [ ] Campaign overview displays

### 3. Test Backend CLI

```bash
dreamtraffic demo
```

Expected: Demo pipeline executes without errors

## Monitoring

### Frontend
- Vercel Analytics (if using Vercel)
- Browser console for client-side errors
- Network tab for API calls

### Backend
- Check agent execution logs
- Monitor Supabase dashboard for queries
- Track API usage (Luma AI, Anthropic)

### Database
- Supabase Dashboard → Database → Logs
- Query performance monitoring
- RLS policy audit logs

## Rollback Procedure

### Frontend
```bash
# Vercel
vercel rollback

# Netlify
netlify rollback
```

### Database
Migrations are one-way. To rollback:
1. Create new migration with reverse changes
2. Apply using Supabase dashboard

## Security Checklist

- [x] RLS enabled on all tables
- [x] Public read-only access for appropriate tables
- [x] Authenticated-only write access
- [x] Environment variables not committed to git
- [x] CORS properly configured
- [x] HTTPS enforced (handled by Vercel/Netlify)

## Cost Estimates

### Supabase (Free Tier)
- Database: ✅ Included
- 500 MB storage: ✅ More than enough
- Bandwidth: ✅ Sufficient for prototype

### Vercel/Netlify (Free Tier)
- Bandwidth: 100 GB/month (Vercel)
- Build minutes: 6000/month (Vercel)
- Cost: $0/month for hobby projects

### APIs (Pay-as-you-go)
- Luma AI: ~$0.01-0.05 per video generation
- Anthropic Claude: ~$0.003 per agent turn (Haiku)

**Total Monthly Cost: ~$0-5 for demo usage**

## Troubleshooting

### Frontend won't load
- Check browser console for errors
- Verify environment variables in hosting dashboard
- Ensure Supabase URL and key are correct
- Check CORS settings in Supabase dashboard

### Backend can't connect to database
- Verify `VITE_SUPABASE_URL` is set
- Verify `VITE_SUPABASE_ANON_KEY` is set
- Check network connectivity
- Test connection with Supabase client directly

### Database queries fail
- Check RLS policies in Supabase dashboard
- Verify table permissions
- Check if reference data was seeded
- Review Supabase logs for detailed errors

## Support

For deployment issues:
1. Check Supabase dashboard logs
2. Review browser console errors
3. Verify all environment variables
4. Check deployment platform logs (Vercel/Netlify)
