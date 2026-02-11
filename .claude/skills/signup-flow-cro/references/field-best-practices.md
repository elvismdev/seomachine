# Signup Form Field Best Practices

## Field-by-Field Optimization

### Email Field
- **Required**: Always
- **Format**: Single input, no confirmation field
- **Keyboard**: `type="email"` for mobile keyboard
- **Validation**: Real-time, inline. Catch typos (gmal.com → gmail.com)
- **Placeholder**: `name@company.com` (not "Enter your email")
- **Autofill**: Support `autocomplete="email"`

### Password Field
- **Show/hide toggle**: Always include — reduces errors by 30%+
- **Requirements**: Show as checklist that updates in real-time, not as error after submission
- **Minimum**: 8 characters is standard. Skip uppercase/special char requirements (they reduce security in practice by encouraging predictable patterns)
- **Meter**: Optional strength meter — useful but not essential
- **Autofill**: Support `autocomplete="new-password"`

### Name Field
- **Single "Name" vs First/Last**: Test this. Single field reduces friction but limits personalization
- **When to split**: If email sequences need "Hi {first_name}" personalization
- **When to combine**: Lead gen, newsletter signup, any low-commitment signup
- **Autofill**: Support `autocomplete="name"` or `given-name`/`family-name`

### Company/Organization Field
- **Make optional** if possible
- **Alternative**: Infer from email domain post-signup (Clearbit enrichment)
- **Auto-suggest**: If required, add company name autocomplete
- **B2B only**: Only include for B2B products. B2C/consumer products should never ask

### Phone Number
- **Avoid if possible**: Phone fields reduce signup rates by 25-50%
- **If required**: Explain why ("We'll text your verification code")
- **Format**: Auto-format as they type. Accept any format
- **Country code**: Auto-detect from IP, allow override
- **Keyboard**: `type="tel"` for mobile

### Job Title/Role
- **Only if needed for routing** (e.g., different onboarding paths)
- **Dropdown preferred**: Reduces input friction
- **Limit options**: 5-8 roles max, plus "Other"
- **Move to onboarding**: Better asked after signup, not during

## OAuth/Social Login

### Best Practices
- **Offer 2-3 options max**: Google + GitHub (for dev tools), Google + Microsoft (for enterprise)
- **Place above email form**: OAuth reduces friction — make it the primary path
- **Clear labels**: "Continue with Google" not "Login with Google" (for signups)
- **Trust signal**: "We'll never post without your permission"

### Recommended OAuth Providers by Product Type
| Product Type | Primary | Secondary |
|-------------|---------|-----------|
| Developer tools | GitHub | Google |
| B2B SaaS | Google | Microsoft |
| Consumer | Google | Apple |
| Education | Google | Microsoft |

## Form Layout Principles

### Field Order
1. OAuth options (lowest friction first)
2. Email (most familiar field)
3. Password (if not using magic link)
4. Name (only if required at signup)
5. Everything else (move to onboarding)

### Visual Best Practices
- Single column layout (always)
- 44px minimum touch targets on mobile
- Visible labels (not placeholder-only)
- Generous spacing between fields (16px+)
- CTA button full-width on mobile

## Benchmarks

| Metric | Good | Great | Best-in-Class |
|--------|------|-------|---------------|
| Signup completion rate | 20-30% | 30-50% | 50%+ |
| OAuth adoption rate | 30-40% | 40-60% | 60%+ |
| Field drop-off per field | 5-10% | 3-5% | <3% |
| Time to complete | 30-60s | 15-30s | <15s |
| Mobile completion rate | 15-25% | 25-40% | 40%+ |
