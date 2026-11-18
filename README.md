# Ready-Set Solutions

Property cleanup and maintenance website for Ready-Set Solutions, operated by CHARLEY'S LLC in Chandler, Arizona.

## One source of truth
- **Website code:** this GitHub repository.
- **Publishing:** GitHub Pages on the main branch, using the existing CNAME.
- **Domain:** readyset.charleysllc.com; this repository does not manage domain renewal or DNS.
- **Inquiries:** contact.html posts to the existing FormSubmit endpoint for readyset@charleysllc.com. Confirm that the destination inbox has approved FormSubmit activation before relying on customer leads.
- **No backend required:** static HTML and styles.css. There is no subscription, checkout, or automated billing system in this repository.

For local prospecting, a 30-day outreach cadence, a private lead-tracking schema, and Stripe invoicing workflow, see [OPERATIONS.md](OPERATIONS.md).

**Billing choice:** A Ready-Set Solutions Stripe account is connected. Use Stripe Dashboard's invoice templates and Stripe-hosted invoice pages after quote approval. There is no need to add Stripe checkout JavaScript to the static website.

## Customer process
1. Receive inquiry with city, property type, service request and contact details.
2. Ask for photos or inspect in person; document access, scope, exclusions, and any hauling requirements.
3. Send an itemized written quote showing labor, materials, permitted third-party hauling/disposal (if relevant), and total price.
4. Obtain customer approval before scheduling or changing scope.
5. Complete work, save before-and-after photos with consent, then send a dated invoice referencing the quote.
6. Record payment and follow up for recurring exterior property care when appropriate.

### Suggested starting prices (business owner must confirm)
- Quick one-time light cleanup: **from $149**, labor only.
- Rental turnover refresh: **from $249**, scoped labor.
- Visual property care visit: **from $89 per visit**.
- No disposal, transport, hazardous waste or permit-requiring services are included in these starter prices.
- These starting prices are advertised, but **not** binding fixed quotes for unseen jobs.

### Example quote/invoice line items
| Item | Quantity | Unit price | Total |
|---|---:|---:|---:|
| Property cleanup labor (scoped area) | 1 | $149.00 | $149.00 |
| Approved materials | As agreed | Itemized | As agreed |
| Permitted third-party hauling | If required | Separately quoted | As agreed |

Invoice should identify the business, invoice number, date, customer, job address, agreed scope, actual approved charges, payment instructions and due date. Use the business's existing compliant invoicing/payment processor; no customer card data should be collected in the website form.

## Before launch / compliance checks
- No business phone number is published yet; add one only once a business-controlled line exists. Confirm readyset@charleysllc.com is business-controlled and the inbox receives FormSubmit inquiries.
- Verify current Arizona Registrar of Contractors license status. The website currently says **Not a licensed contractor**, pending verification; update that statement if a valid license applies. Do not advertise regulated trade work or work requiring permits without appropriate licensing. Arizona's handyman exemption is generally limited to projects under $1,000 including labor and materials and no permit requirement.
- Confirm city-specific rules and required permits for commercial waste hauling; Chandler has a separate commercial waste-hauler permit process. Arrange authorized haulers rather than assuming pickup or landfill privileges.
- Check business insurance, taxes, and municipal rules for any added service.
- Publish genuine reviews only after verifying customer permission and substantiating ratings; old unverified testimonial/rating copy has been removed.
- Update pricing when real job-cost data supports it.

## Pages
- index.html: single clear service menu, public starting prices, coverage, and estimate workflow.
- contact.html: lead intake.
- thank-you.html: form return page.
- privacy.html: disclosure.
- indoor.html, outdoor.html, reviews.html, services/index.html: safe legacy pages; marked noindex and linked to current services.
- sitemap.xml: only current public pages.

## Keep it simple
Do not add another hosting service, e-commerce integration, or software subscription unless there is a specific need. The next useful operational tool is an invoicing system and a private lead tracker, not another website host.
