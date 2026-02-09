# Data Pipeline API Setup Guide

## Required Credentials

All credentials go in `data_sources/config/.env`.

### Google Analytics 4 (GA4)

```
GA4_PROPERTY_ID=properties/123456789
GA4_CREDENTIALS_PATH=credentials/ga4-credentials.json
```

1. Create a service account in Google Cloud Console
2. Enable the Analytics Data API
3. Grant the service account Viewer access to your GA4 property
4. Download the JSON key file to `credentials/ga4-credentials.json`

### Google Search Console (GSC)

```
GSC_SITE_URL=https://yoursite.com/
GSC_CREDENTIALS_PATH=credentials/ga4-credentials.json
```

Uses the same service account as GA4. Grant it access in GSC.

### DataForSEO

```
DATAFORSEO_LOGIN=your-login
DATAFORSEO_PASSWORD=your-password
```

Sign up at dataforseo.com for API credentials.

## Testing Connectivity

```bash
python3 test_dataforseo.py
```

## Graceful Degradation

The data aggregator automatically skips unavailable data sources:
- If GA4 is not configured: traffic data is omitted
- If GSC is not configured: search data is omitted
- If DataForSEO is not configured: SERP data is omitted

The system always works — you just get richer data with more credentials configured.
