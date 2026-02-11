# Popup Compliance & GDPR Guide

## GDPR Requirements for Popups

### Consent Rules
- **Pre-checked boxes are illegal**: Opt-in checkboxes must be unchecked by default
- **Bundled consent is invalid**: Marketing consent must be separate from terms acceptance
- **Clear language**: "Send me marketing emails" not "Stay updated with our communications"
- **Easy withdrawal**: Unsubscribe must be as easy as subscribing

### Required Elements
1. **Clear purpose**: State what you'll do with their data
2. **Privacy policy link**: Visible and accessible
3. **Consent mechanism**: Explicit opt-in (not pre-checked)
4. **Data controller identity**: Who is collecting the data

### Cookie Consent Interaction
- Email popups that set tracking cookies need cookie consent FIRST
- Sequence: Cookie consent banner → (accepted) → Email popup
- Don't show marketing popups to users who haven't accepted cookies

## Google Interstitial Guidelines

### What Google Penalizes (Mobile)
- Full-screen popups before content loads
- Standalone interstitials users must dismiss before accessing content
- Above-the-fold layouts where content is pushed below a popup-like element

### What Google Allows
- Cookie consent notices (legally required)
- Age verification gates (legally required)
- Banners that use a reasonable amount of screen space
- Login dialogs for paywalled content

### Safe Popup Patterns for SEO
- **Bottom slide-ins**: Don't cover content, easy to dismiss
- **Scroll-triggered**: Only shown after engagement (50%+ scroll)
- **Exit intent**: Triggered on leave, not on entry
- **Click-triggered**: User-initiated (zero SEO risk)

## CCPA (California) Requirements

- **"Do Not Sell" link**: Required if selling personal information
- **Opt-out mechanism**: Must be honored within 15 days
- **Privacy notice**: At or before the point of collection
- **No discrimination**: Can't penalize users who opt out

## CAN-SPAM (US Email)

- **Clear sender identification**: Who the email is from
- **Accurate subject lines**: No deception
- **Physical address**: Required in every email
- **Unsubscribe mechanism**: Must work for 30 days after send
- **Honor opt-outs**: Within 10 business days

## Accessibility Requirements (WCAG 2.1)

### Popup Accessibility Checklist
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Focus trapped inside popup while open
- [ ] Focus returns to trigger element on close
- [ ] `role="dialog"` and `aria-modal="true"`
- [ ] `aria-labelledby` pointing to popup heading
- [ ] Close button has accessible name ("Close" not just "X")
- [ ] Sufficient color contrast (4.5:1 for text)
- [ ] Works with screen readers
- [ ] No content conveyed by color alone
- [ ] Touch targets at least 44x44px on mobile

## Implementation Checklist

### Before Launch
- [ ] Privacy policy updated to cover popup data collection
- [ ] Cookie consent integrated (EU/UK visitors)
- [ ] Opt-in mechanism is explicit (not pre-checked)
- [ ] Unsubscribe mechanism tested
- [ ] Mobile popup doesn't violate Google interstitial guidelines
- [ ] Popup is keyboard accessible
- [ ] Screen reader compatible
- [ ] CCPA "Do Not Sell" link present (if applicable)

### Ongoing
- [ ] Monthly audit of consent records
- [ ] Quarterly review of popup compliance
- [ ] Honor data deletion requests within 30 days
- [ ] Update privacy policy when data practices change
