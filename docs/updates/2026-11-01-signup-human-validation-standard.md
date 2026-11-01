# Signup human-validation requirements

Added a technical-specification reference for the web and Android signup defaults: Turnstile with mandatory backend verification for browsers; Firebase App Check with Play Integrity for Android distributed through Google Play; and a Turnstile WebView fallback when expected attestation cannot be obtained. The reference adds acceptance evidence for invalid, expired, replayed, wrong-host, outage, retry, debug, emulator, sideload, and release-build cases.

The controls address bot-driven and unauthorised automated use and remain complementary to authentication, authorisation, email confirmation, rate limits, and privacy review. Current provider claims were checked against official Cloudflare and Firebase documentation on 1 November 2026, with a review date of 1 February 2027.
