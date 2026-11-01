# Signup Human Validation Requirements

Parent skill: [technical specification](../SKILL.md). Use when specifying account creation, signup verification, or signup-related resend flows for web and Android clients.

## Platform pattern

| Client | Required design default | Acceptance evidence |
|---|---|---|
| Web browser | Cloudflare Turnstile Managed mode; the backend verifies tokens with Siteverify and checks the expected hostname. | Tests show valid tokens pass, while invalid, missing, expired, duplicate, and wrong-host tokens fail safely. |
| Android distributed through Google Play | Firebase App Check with the Play Integrity provider; the backend verifies the App Check token against the expected project and app. | A Play-installed release build passes; invalid or missing attestation is rejected when enforcement is active. |
| Android unable to obtain the expected Play attestation | Offer a Turnstile WebView fallback with a clear retry path. | Fallback succeeds on supported devices and does not expose server secrets to the app. |
| Development and test builds | Use provider-supported test or debug credentials only in non-production builds. | Build and configuration checks prove test providers cannot be enabled in production. |

## Cross-cutting requirements

- Treat these as complementary bot and unauthorised-automation controls, not identity proof or replacements for authentication, authorisation, or business-level access checks.
- Offer the Android Turnstile fallback when expected Play attestation cannot be obtained; an invalid attestation remains a failure.
- Apply the verification decision to registration and signup-related resend endpoints before creating pending accounts or sending messages.
- Preserve independent controls such as rate limits, email confirmation, and suitable honeypots. Device identifiers are not proof of an authentic app.
- Keep secrets server-side; separate credentials by environment; restrict web widgets to approved hostnames.
- Treat invalid, expired, and replayed tokens as failures. During a confirmed provider outage, allow a pending signup only under stricter limits and mandatory email confirmation, with logging, alerting, a named owner, and a rollback or expiry. Never record an outage-path request as verified.
- Roll out through monitor and staged enforcement where supported. Define measured exit criteria from real-device failure rates, signup completion, support complaints, and provider errors.
- Include normal, failure, retry, low-connectivity, unsupported-device, and service-outage cases in the test plan. Use current provider test tools outside production.
- Assess privacy notices and applicable app-store disclosures for provider data flows; route jurisdiction-specific conclusions to the authorised privacy or legal reviewer.

## Currentness record

Official provider documentation was checked on 1 November 2026. Review by 1 February 2027 or when the integration or provider changes.

- Cloudflare, [Server-side validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/), updated 16 September 2026: server verification is required; tokens are single-use and valid for 300 seconds. Scope: Turnstile. Status: verified on 1 November 2026; recheck before implementation.
- Cloudflare, [Mobile implementation](https://developers.cloudflare.com/turnstile/get-started/mobile-implementation/), updated 5 May 2026: native apps use a WebView for Turnstile. Scope: documented mobile integration. Status: verified; device performance remains project-specific and requires testing.
- Firebase, [Play Integrity provider](https://firebase.google.com/docs/app-check/android/play-integrity-provider/) (updated 28 October 2026) and [custom backend verification](https://firebase.google.com/docs/app-check/custom-resource-backend/) (updated 6 October 2026): App Check can use Play Integrity on Android and custom backends must verify tokens. Scope: Firebase App Check. Status: verified on 1 November 2026; project setup, quota, signing and SDK compatibility remain implementation-time checks.
