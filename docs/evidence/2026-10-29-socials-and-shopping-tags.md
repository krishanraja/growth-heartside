# Shopping tags and social launch readiness: closeout, 29 October 2026

Brief: `docs/briefs/2026-10-29-heartside-shopping-tags.md`
Worked in Krish's signed-in Chrome and the built-in browser pane, with Krish approving each account, sales-channel and permission change at the moment it happened.
Filed by the growth engine session from Cowork's closeout. Left out because this repository is public: one security notice, which went to Krish directly, and notes about the signed-in browser.

## Why this mattered

The brief's goal: someone sees the mug, blanket or portrait in a post, taps the product tag, and lands on the right product page with its price. Clicks from those tags must arrive with the platform as referrer and count as organic social.

The North Star is Shopify net sales, trailing four weeks, with a ladder that starts at $250 for the week of 26 October and rises to $50,000 by 22 February 2027. On 28 October the figure was $24, so organic social has to start carrying traffic now.

## Outcome against the brief's "done when"

| Platform | Tag a post with all three gifts | Tag opens right page with price | Status |
|---|---|---|---|
| Pinterest | Yes, proven with a live test Pin | Yes, all three, Pinterest as referrer | **Done** |
| Instagram | Not yet | n/a | Waiting on Meta Commerce review |
| Facebook | Not yet | n/a | Waiting on Meta Commerce review |
| TikTok | Will not tag | n/a | **Deliberately held** by Krish's ruling below |

All four accounts are ready to post today. Each is signed in as `yourdoghasnotes` with the heart avatar, name, bio and a route to heartside.io. Organic posts and paid ads that link to heartside.io work on all four now. Only selling inside the apps, through tags and in-app checkout, waits on the reviews.

## Rulings and decisions made in this session

1. **TikTok Shop: hold, no products listed** (Krish, 29 October). TikTok Shop checks out inside the app and gives the buyer nowhere to upload a dog photo. Heartside's product only works if the photo and Buddy's painting come before checkout. Listing there would take orders that cannot be made. TikTok also expects standard orders to ship within 2 business days. Revisit only if a post-purchase photo collection flow exists and Krish asks. Until then, TikTok sells by sending people to heartside.io through posts, the bio and ads.
2. **Artist's touch stays off the social catalogs** (Krish approved). It is an add-on and should never appear as a standalone shoppable item. It is now published on the Online Store only. Unpublishing through the API was blocked by a safety policy, so this was done in Shopify's "Manage publishing" screen.
3. **One avatar across all four profiles:** the brand-book pink watercolor heart with the white paw. The source is the live heart favicon on heartside.io, centered and unchanged on brand cream #FBF6F1. Approved under Krish's "align it to the best of your ability". The brand book says not to improvise a Buddy avatar, so none was made.
4. **Test Pin published** (Krish approved): it is labeled "AI modified" because the product paintings are AI-made. That label is an honest default, not a ruling, and Krish can turn it off.

## What each platform needed

### Meta (Facebook and Instagram)
- Installed Shopify's Facebook & Instagram channel and connected the Heartside Facebook Page and the `yourdoghasnotes` Instagram business account. Connected the existing Meta catalog and pixel with Maximum data sharing, then submitted the shop for Commerce review.
- Status in Shopify: "We're reviewing your shop", with products syncing. Meta says the full review can take up to four weeks, so expect a decision by about 26 November.
- Ads on Facebook and Instagram show "Active" and can run to heartside.io now.
- Catalog: the mug, blanket and portrait are published to the channel, and Artist's touch is not.
- A paid third-party app, MetaShop (£7.49 per 30 days), is installed and was left untouched. Decide separately whether it is still needed now that the official channel is connected.

### Pinterest
- Converted Krish's existing Pinterest account to a free business account, profile `yourdoghasnotes`, after he accepted the Business Terms.
- Installed Shopify's Pinterest channel, linked the business account and accepted the tag and Conversions API terms. That installed the Pinterest tag and auto-created an ad account. No billing and no spend.
- heartside.io is claimed (green check). The catalog is approved: 11 items, none rejected.
- Fixed the profile website, which the Shopify connection had switched to the myshopify domain, back to heartside.io.
- A merchant review on the app store reported a domain being flagged as spam after integrating. Keep an eye on domain status.
- **Test Pin**, published on the board "Gifts from your dog", with all three gifts tagged:
  - Main link: `https://heartside.io/?utm_source=pinterest&utm_medium=social&utm_campaign=test-pin`
  - The Pinterest API confirms all three tags point at the right product URLs.
  - Each tag clicked through from pinterest.com:

  | Tag | Page | Price | Referrer |
  |---|---|---|---|
  | Mug | Your Dog's Illustrated Mug | $45.00 | pinterest.com |
  | Blanket | Your Dog's Personality Blanket | $129.00 | pinterest.com |
  | Portrait | Your Dog's Portrait | $119.00 framed, the default; $59 unframed on the same page | pinterest.com |

  - The tags don't show prices inside Pinterest yet. The product pages publish the correct `og:price` (45.00, 129.00, 59.00 USD), so Pinterest should fill them in on its next refresh. **Check on 30 October.**

### TikTok
- Shopify's TikTok channel was already installed, but it is not connected to the shop and no products are published to it.
- The TikTok Shop US application was first held for proof of address, which was not a London-registration block. Krish supplied it himself, and the application is now **under review**, sitting at "Add your first product". Per the ruling above, nothing was listed.
- Bio aligned to: "Your dog loves you too. Gifts from your dog. Free US shipping. heartside.io".
- The display name stays "Heartside: Gifts from your dog". The full name is over TikTok's 30-character limit, and TikTok only allows a name change every 7 days.
- "heartside.io" in the bio is plain text. TikTok's website showed no website field for this account; if the app's edit profile offers one, Krish should add the link there.

### Shopify payments (checked because the repo status notes flagged it)
- Shopify Payments shows Accepting payments and Receiving payouts, with no test mode, and the Bogus Gateway is no longer listed. Checkout offers Shop Pay, Apple Pay and Google Pay. **The store can take real payments.** This settles the 28 October worry that payments were left off after the mock orders. The rest of the CoWork acceptance run is a separate matter and was not checked here.

## Brand alignment across the four profiles

| | Instagram | Facebook Page | TikTok | Pinterest |
|---|---|---|---|---|
| Handle | yourdoghasnotes | yourdoghasnotes | yourdoghasnotes | yourdoghasnotes |
| Name | Heartside: Personalized Dog Gifts | Heartside: Personalized Dog Gifts | Heartside: Gifts from your dog (limit) | Heartside: Personalized Dog Gifts |
| Avatar | Heart and paw | Heart and paw | Heart and paw | Heart and paw |
| Bio | Your dog loves you too. Gifts from your dog, in your dog's own words. Free US shipping. | Same | Your dog loves you too. Gifts from your dog. Free US shipping. heartside.io | Your dog loves you too. Gifts from your dog: an illustrated mug, a sherpa blanket and a portrait, made from your dog's photo. |
| Link | heartside.io with Instagram UTM | heartside.io | Plain text only | heartside.io (claimed) |

Facebook's page-setup checklist (address, phone, hours) was left unfinished on purpose. Heartside is online-only.

## Tracking (brief step 4)
- The store's UTM handling is unchanged.
- Pinterest product-tag clicks arrive with `pinterest.com` as the referrer, which Shopify reports as social. Tag links carry no UTM, so attribution relies on the referrer. The Pin's main link carries UTMs.
- Instagram and Facebook tag clicks can't be tested until Meta approves the shop. Rerun the same click-through test then.

## Waiting on platforms

| What | Expected | Next action |
|---|---|---|
| Meta Commerce review | By about 26 November | When approved, tag all three gifts on one Instagram post and one Facebook post, then click through to check page, price and referrer |
| Prices on the Pinterest tags | 30 October | Reopen the test Pin and confirm all three tags show prices |
| TikTok Shop application | Days | Approval changes nothing while the hold stands |

## Waiting on Krish
- **MetaShop app:** keep or remove the £7.49 per 30 days app.
- **Pinterest billing:** only if he wants Pinterest ads. Note the "Get your credit" ad-credit offer opts into the offer and starts campaign creation, so it is not a free toggle.
- **Portrait default:** the product page opens on framed at $119. Decide whether tagged traffic should land on unframed at $59, the entry price shown everywhere else.

## Cautions for the next session
- **The Drive file `favicon-512.png` is not the heart icon.** It is an illustrated dog, a Buddy-style drawing. The brand book says not to improvise Buddy art, so don't use it as an avatar. The approved heart is the site favicon, `heartside-favicon-heart.png`, 512 px with a transparent background. Avatars need the cream background added so the heart doesn't sit on black.
- The built-in browser pane can't upload files and blocks popups. Do uploads in Chrome.
- **Never use the TikTok Shop UK seller registration.** Krish landed on it once. It would start a second application. The US Seller Center is the only one.

## Evidence
- Shopify Admin API readback: the mug, blanket and portrait are published to Online Store, Facebook & Instagram and Pinterest. Artist's touch is on Online Store only. Nothing is on TikTok.
- Shopify Pinterest overview: catalog Connected, 11 approved, 0 not approved.
- Shopify Facebook & Instagram overview: "We're reviewing your shop", ads "Active".
- Shopify Payments settings: Accepting payments and Receiving payouts, no test mode.
- Pinterest test Pin data: three tags with the right product URLs. Click-through results are in the table above.
- Profile pages read back on all four platforms after each change.

North Star check (2026-10-29): holds. This work removes channel blockers and adds no spend. The number moves only once posting starts.
