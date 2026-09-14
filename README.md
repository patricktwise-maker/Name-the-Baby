# Name the Baby V11 — Public Launch Polish + Monetization

The visitor-facing product remains one page.

## V11 upgrades

### Live ballot polish
- remembers a browser's existing vote on each ballot
- reopens live results for returning voters
- one browser token remains one vote in Supabase
- tapping a different name changes that vote rather than adding a second vote
- live percentage bars and vote counts
- highlights the current leader(s)
- clearer ballot ID and live-status messaging

### Monetization
Three launch partnership positions:
1. Founding Sponsor
2. Category Partner
3. Featured Partner

Sponsor inquiries still flow into the existing private Supabase sponsor-inquiry table.
The selected package is included in the submitted inquiry.

### Affiliate / partner-ready name moment
Each generated name now exposes a restrained contextual placement such as:
"Personalize Micah"
The public launch version does not fake an affiliate offer. Until a real partner exists,
the button routes to the sponsorship inquiry flow.

### Brand polish
- refined wordmark lockup
- launch-capability badges
- cleaner ballot results
- clearer sponsor value proposition

## Production backend
This build inherits the browser-safe Supabase Project URL and publishable key from V10.1.
No secret/service-role/database password is shipped to the browser.

## Deployment
Deploy this V11 folder to Vercel. It can replace the V10.1 public build.
