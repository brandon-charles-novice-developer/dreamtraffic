# DreamTraffic Frontend

React prototype for the DreamTraffic creative pipeline visualization.

## Quick Start

```bash
npm install
npm run dev
```

## Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## Deploy

### Vercel (Recommended)

```bash
vercel --prod
```

Set environment variables in Vercel dashboard:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

### Netlify

```bash
netlify deploy --prod
```

Set environment variables in Netlify dashboard:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## Environment Variables

Create a `.env` file:

```env
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

## Tech Stack

- **React 19** - UI framework
- **Vite 6** - Build tool
- **Tailwind CSS 3** - Styling
- **Supabase** - Database client

## Features

- Campaign overview dashboard
- Creative studio with video previews
- Approval workflow visualization
- DSP trafficking status
- Supply chain fee analysis
- VAST tag inspector

## Development

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

## Project Structure

```
prototype/
├── src/
│   ├── components/     # React components
│   ├── data/          # Mock data
│   ├── lib/           # Supabase client
│   ├── App.jsx        # Main app component
│   └── main.jsx       # Entry point
├── public/            # Static assets
└── dist/              # Production build
```
