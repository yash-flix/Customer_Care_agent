import streamlit as st
import subprocess
import json
import re
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Lauki Support",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Knowledge Base (CSV-backed fallback)
# -----------------------------
KNOWLEDGE_BASE = {
    "What plans do Lauki Phones offer?": "Prepaid, postpaid, family, enterprise, and data-only plans. Each tier defines fixed data limits, voice allowances, roaming eligibility, renewal rules, and addon compatibility. Enterprise plans include device management APIs and priority support.",
    "How do I activate a new SIM?": "Insert the SIM, complete KYC with government-issued ID, verify phone number ownership, and restart the device. Network registration finishes once identity and address checks clear.",
    "How long does activation take?": "Activation completes within 30 minutes in most regions. Delays occur only when KYC verification needs manual review or when the device fails to register on a supported band.",
    "Does Lauki Phones support eSIM?": "Supported on devices that follow GSMA eSIM standards. Provisioning occurs through the Lauki Phones portal, which issues a single-use QR profile tied to the account.",
    "How do I switch from physical SIM to eSIM?": "Authenticate in the portal, request conversion, validate identity, and scan the generated QR on the device. The physical SIM deactivates immediately after profile installation.",
    "How do I check my data balance?": "The app dashboard shows real-time usage, daily consumption, and projected depletion. The USSD balance code provides a fallback when mobile data is unavailable.",
    "How do I upgrade my plan?": "Select an eligible higher-tier plan in the app. System recalculates prorated charges, locks the new plan for the next billing cycle, and adjusts data and voice limits at cycle start.",
    "What is the billing cycle for postpaid?": "Billing begins on the customer's activation date and repeats every 30 days. Overages, roaming usage, and addons reflect in the next invoice with itemized entries.",
    "How do I pay my bill?": "Supported methods include UPI, credit/debit cards, net-banking, and autopay. Autopay triggers on invoice generation to avoid service interruption for overdue accounts.",
    "Are international roaming packs available?": "Roaming packs cover APAC, EU, Middle East, and Americas. Each pack specifies data caps, voice allowances, validity periods, and country-specific restrictions.",
    "How do I activate international roaming?": "Purchase a region-specific roaming pack and enable roaming in device settings. System pushes roaming credentials to the visited network within minutes.",
    "Does Lauki Phones throttle speeds after data limits?": "Yes. Once the plan's fair-usage data limit is exceeded, speeds drop to the published throttle rate. Full speeds resume only after renewal or purchase of a data addon.",
    "Can I share data with family members?": "Family plans allow a single data pool managed by the primary account holder. Allocation can be set per member or left dynamic based on real-time usage.",
    "How do I report network issues?": "File a ticket in the app specifying location, timestamps, and issue type. The diagnostic engine runs automated checks before forwarding the case to field teams.",
    "What should I do if my SIM is lost?": "Block the SIM through the account portal to disable all network access. Request a replacement after verifying identity to prevent unauthorized usage.",
    "Is SIM replacement chargeable?": "Yes. Replacement fees cover SIM provisioning, KYC validation, and backend reprofiling. Charges differ by region but stay within the regulated upper limit.",
    "Does Lauki Phones support VoLTE?": "VoLTE is enabled for devices certified on Lauki Phones' IMS network. High-definition calling activates automatically when LTE coverage is available.",
    "Does Lauki Phones support WiFi Calling?": "Supported for most current smartphones. Calls route through secure IMS tunnels when cellular coverage is weak, maintaining voice quality and call continuity.",
    "How do I enable WiFi Calling?": "Enable WiFi Calling in device network settings and connect to a stable WiFi network. The device registers with the IMS server once authentication succeeds.",
    "How do I transfer my number from another carrier?": "Submit a porting request using the port code issued by the current carrier. Lauki Phones validates identity, initiates number transfer, and schedules activation.",
    "How long does porting take?": "Porting completes within 3–5 working days. During the final transfer window, short downtime occurs while routing shifts from the old carrier to Lauki Phones.",
    "Can I pause my service temporarily?": "Temporary suspension is available for up to 90 days. Suspended accounts retain the number but lose active services until reactivation.",
    "How do I change my registered address?": "Upload updated address proof, complete digital verification, and wait for backend validation. Address changes update billing and regulatory records.",
    "Are corporate discounts available?": "Yes. Enterprise accounts receive volume-based discounts, pooled data options, centralized billing, and SLA-bound support.",
    "How do I get itemized call and data usage?": "Download the usage statement from the billing dashboard. The report lists timestamps, duration, data sessions, roaming events, and cost attribution.",
    "Does Lauki Phones offer 5G?": "5G is available on compatible devices and plans. Access depends on local coverage, device band support, and the customer's plan tier.",
    "How do I verify if my device is compatible?": "Open the Lauki Phones app and navigate to Device Check under Settings. The system reads your device model via IMEI, modem capabilities, and supported band lists, then cross-validates them against the active network profile. If incompatible, the app suggests alternatives like band-unlocking services or compatible device recommendations.",
    "Can I order a SIM online?": "Yes. Log into your Lauki Phones account, submit KYC details including PAN and Aadhaar, select a delivery slot, and complete address verification via OTP. The physical SIM or eSIM QR code ships with tamper-evident packaging. Activation remains pending until identity and address proofs clear, typically within 24–48 hours.",
    "What ID documents are accepted for KYC?": "Lauki Phones accepts Aadhaar Card, Voter ID, PAN Card, international passports with valid visas, and driver's licenses from recognized authorities. Documents must include a clear photo, signature, and current residential address updated within the last 6 months. DigiLocker integration is supported for faster digital verification.",
    "How do I enable autopay?": "Go to Billing Settings in the app or portal, register a preferred payment method, authorize recurring charges via PIN or OTP, and confirm the mandate. You'll receive a confirmation email with mandate details and the first charge date aligned to your billing cycle.",
    "Can I disable autopay anytime?": "Yes. Disable autopay from the Billing section by selecting the active mandate and confirming cancellation via OTP. The change applies instantly. Any unpaid invoices from the current cycle must be settled manually.",
    "What happens if my bill is overdue?": "Services enter a 7–10 day grace period with full access maintained but daily reminders sent. Post-grace, outbound usage is restricted. Continued non-payment after 15 days leads to full suspension of voice, data, and roaming until dues are cleared.",
    "How do I download past invoices?": "Access past invoices in the Billing History tab, covering up to 24 months of records. Each PDF includes tax breakdowns, plan charges with prorated adjustments, itemized usage, and promotional credits. Filter by date or invoice number for quick retrieval.",
    "Are there late payment fees?": "Yes. A fixed fee of ₹50–100 applies after the grace period, escalating to 1.5% daily interest on the outstanding amount thereafter, in line with TRAI mandates. Fees are waived for first-time delays under 5 days or proven technical glitches.",
    "How do I dispute a bill charge?": "Submit a ticket via the Support section in the app with supporting evidence such as usage logs or payment screenshots. Billing teams review CDRs, rating engine outputs, and network logs within 7–10 business days before issuing corrections or credits.",
    "Can I set usage alerts?": "Yes. Set thresholds in the Usage Controls menu for data, voice, and roaming categories. Notifications trigger via in-app banners, push alerts, email, and SMS with customizable frequencies.",
    "Can I restrict data usage for family members?": "As the primary account holder, access the Family Dashboard to assign fixed data caps, block international roaming data, or temporarily disable high-speed data for specific lines. Restrictions apply instantly with override options via PIN.",
    "How do I enable parental controls?": "Enable parental controls through the Family Management module: select the child's line, enforce age-based content filters, set app-level restrictions, and apply time-based rules. Setup requires a one-time PIN and activity logs are available for review.",
    "Does Lauki Phones support number masking?": "Yes, for eligible enterprise accounts. Number masking anonymizes caller IDs during support calls or SMS campaigns using dynamic virtual numbers routed through the IMS core. Available in 50+ countries under GDPR/CCPA standards.",
    "Does the service support static IP addresses?": "Static IP addresses are available for enterprise mobile broadband connections upon request, subject to network feasibility. Allocation involves a one-time setup fee and annual renewal with IPs from a /24 subnet pool.",
    "What security measures protect my account?": "Your account is protected by MFA with biometric or hardware keys, device binding, end-to-end TLS 1.3 encryption, real-time SIM swap alerts, and AI-driven anomaly detection. Security audits comply with ISO 27001 and zero-trust architecture.",
    "How do I reset my account password?": "Select Forgot Password on the login screen. Verification occurs via OTP to your registered mobile or email, fallback security questions, or device biometrics. The new password must meet complexity rules of 12+ characters with mixed types.",
    "Can I block spam calls and SMS?": "Lauki Phones employs a network-level AI spam filter blocking over 90% of known fraudulent sources. Users can enable device-level filtering in the app for custom blacklists or report spam numbers via *123# USSD.",
    "What happens during network maintenance?": "Scheduled maintenance, typically 2–4 hours monthly between 2–5 AM local time, may cause brief service degradation. Critical services remain prioritized. Customers receive 48-hour advance notice via app and SMS.",
    "How do I request a coverage check for my area?": "Submit your postcode and device details in the Coverage Map tool in the app or website. Field teams analyze tower load metrics and signal quality KPIs before confirming eligibility or scheduling optimizations. Responses arrive within 72 hours.",
    "How do I move my service to a new device?": "Power off the old device, insert the physical SIM or scan the eSIM QR code on the new device, then restart. The network detects the change via IMSI and reprofiles capabilities automatically. Full handover completes in under 2 minutes.",
    "Can I change my mobile number?": "Yes. Request via the Profile section with identity verification through OTP and KYC re-submission. The new number updates across billing, app login, and service logs within 4 hours, with a 7-day grace period for notifying contacts.",
    "How can I block international calls?": "Toggle the permission in Call Settings in the app. Options include full block, whitelist exceptions, or time-based limits. The update syncs to your IMS profile in real-time via OTA.",
    "Does Lauki Phones support conference calling?": "Yes, for up to 5–10 participants depending on the plan's voice profile. Initiate via the dialer or app button. Enterprise plans add recording and transcription add-ons.",
    "How do I enable call forwarding?": "Enable in your device's native call settings or via the Lauki app's Forwarding Rules for advanced conditional options. Rules update on the IMS server in real-time, supporting up to 3 forwarding numbers.",
    "Can I view my porting status?": "Yes. Track porting status in the Porting tab of the app showing real-time progress: initial validation 1–2 days, donor carrier approval up to 3 days, and final activation within 4 hours of approval.",
    "What happens if porting is rejected?": "Rejections stem from invalid port-out codes, mismatched KYC IDs, outstanding dues above ₹100, or recent number changes within 90 days. You'll receive the exact reason and resolution steps via SMS and email.",
    "Are data-only SIMs supported?": "Yes, data-only SIMs exclude voice and SMS to focus on high-speed connectivity for routers, tablets, IoT sensors, and dongles. Plans start at 10GB/month with no throttling up to the fair usage policy limit.",
    "Does Lauki Phones offer device financing?": "Lauki Phones offers financing for selected devices through partnered banks, requiring CIBIL score above 700. EMI terms range from 6–24 months at 0–12% interest with bundled plans reducing effective costs.",
    "How do I track order delivery?": "Track your device or SIM order in the Orders section of the app with real-time GPS updates from logistics partners, including pickup scans, transit milestones, and ETA adjustments.",
    "Is there a lock-in period for plans?": "Prepaid plans have no lock-in. Postpaid plans may include a 6–12 month minimum tenure for discounted rates or device bundles, with early exit fees prorated. Unlimited plans are lock-in free but require 30-day notice for changes.",
    "How do I unsubscribe from promotional messages?": "Unsubscribe in Notification Settings by toggling off marketing categories. Opt-outs process instantly via DND registry integration, applying to SMS, email, and push while exempting mandatory regulatory alerts.",
    "Can I request detailed roaming rates?": "Yes. Access detailed roaming rates in the Roaming section with per-country breakdowns for data, voice, and SMS, including pack options. Rates update quarterly and a rate simulator tool previews costs.",
    "How do I optimize roaming usage?": "Enable roaming only via app toggle when traveling, purchase valid packs, restrict background data in device settings, and monitor real-time usage from the dashboard. Use Wi-Fi calling where available to offload cellular data.",
    "Do enterprise accounts get API access?": "Yes. Enterprise plans include RESTful APIs for device lifecycle management, usage analytics, provisioning, and number masking. SDKs for Python and Node.js are available with OAuth2 security and 99.9% uptime SLAs.",
    "How do I escalate an unresolved issue?": "Escalations follow a tiered SLA: frontline chat or email resolves within 24 hours, network operations handles technical faults within 48 hours, and regulatory compliance covers billing or privacy within 72 hours. Use the Escalate button in open tickets.",
    "Does Lauki Phones provide IPv6 connectivity?": "IPv6 is enabled by default on LTE and 5G networks for compatible devices using dual-stack mode. Benefits include larger address pools for IoT and reduced NAT overhead.",
    "How do I activate voicemail?": "Activate voicemail in the app's Voice Settings or via USSD code *86. Setup prompts greeting recording, PIN creation, and notification preferences. Stores up to 20 messages with auto-forward on full mailbox.",
    "How do I retrieve voicemail?": "Open the dedicated tab in the Lauki app for transcriptions and playback, or dial 123 from your line. Messages sync across linked devices in real-time with options to save, export, or forward.",
    "Are emergency numbers accessible without balance?": "Yes. Emergency numbers including 100, 101, 112 in India and 911 in the US are always accessible without balance, plan status, or SIM restrictions. Location data is shared automatically for faster response.",
    "Can I transfer ownership of my number?": "Transfer ownership by both parties submitting KYC forms and a signed digital declaration in the app. Post-regulatory review takes approximately 7 days, after which the number shifts with prorated balance and bills intact.",
    "Do prepaid plans auto-renew?": "Prepaid plans auto-renew at cycle end if sufficient balance exists. Failed renewals due to low funds suspend benefits until recharge, with grace SMS reminders 24 hours prior.",
    "How do I check my recharge history?": "View recharge history in the Transactions section with entries listing timestamps, payment method, amount, reference numbers, and validity added. Filter by date range or type and export to CSV.",
    "Does Lauki Phones support hotspot tethering?": "Yes. Hotspot usage counts toward your plan's data allowance. Lower-tier plans may rate-limit speeds to 2Mbps after 10GB tethered, while unlimited tiers allow full-speed sharing.",
    "Can I track device usage across SIMs?": "Yes. The Analytics Dashboard tracks usage across multiple SIMs and devices, breaking down data volume, network type, session category, and time periods with visual charts and exportable reports.",
    "What happens if I exceed voice minutes?": "Exceeding voice minutes triggers per-minute overage billing at the plan rate, itemized in your next invoice. Fair usage policies cap excessive calls at 500 minutes per day.",
    "Are unused data benefits rolled over?": "Unused data rolls over to the next cycle on selected prepaid plans at 50% rollover up to 10GB, and fully on postpaid loyalty tiers up to the plan's cap. Rollover activates automatically at renewal.",
    "Can I purchase multiple addons?": "Yes. Stack multiple addons via the Addons store, each with independent validity and usage buckets. Up to 5 active addons per line, with a summary view in the dashboard.",
    "How do I deactivate an addon?": "Addons deactivate automatically at validity end. Mid-cycle deactivation is not supported once activated. Contact support for prorated refunds on valid cases such as app glitches.",
}

# -----------------------------
# Fuzzy Keyword Matcher (fallback when agentcore is unavailable)
# -----------------------------
def kb_lookup(query: str) -> str:
    q = query.lower().strip()
    # Direct match
    for key, val in KNOWLEDGE_BASE.items():
        if key.lower() == q:
            return val
    # Keyword scoring
    scores = []
    q_words = set(re.findall(r'\w+', q))
    for key, val in KNOWLEDGE_BASE.items():
        k_words = set(re.findall(r'\w+', key.lower()))
        score = len(q_words & k_words)
        scores.append((score, key, val))
    scores.sort(reverse=True)
    if scores and scores[0][0] >= 2:
        return scores[0][2]
    return (
        "I wasn't able to find a specific answer in the knowledge base for that query. "
        "For further assistance, you can reach our support team at 1800-XXX-XXXX (toll-free, 9 AM–9 PM) "
        "or raise a ticket through the Lauki Phones app under Support > New Ticket."
    )

# -----------------------------
# Avatar Configuration
# -----------------------------
USER_AVATAR = "human_avatar.svg"
ASSISTANT_AVATAR = "ai_avatar.svg"

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', Inter, sans-serif;
    background-color: #000000;
    color: #FAFAFA;
}

.main { background-color: #000000; }

.block-container {
    max-width: 820px;
    padding-top: 0rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    padding-bottom: 0rem;
}

/* ─── Sidebar ─────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #080808 !important;
    border-right: 1px solid #1A1A1A !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

.sidebar-brand {
    padding: 22px 22px 18px;
    border-bottom: 1px solid #1A1A1A;
    margin-bottom: 0;
}

.brand-name {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: #FAFAFA;
    text-transform: uppercase;
}

.brand-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #C0C0C0;
    letter-spacing: 0.06em;
    margin-top: 5px;
}

.sidebar-section {
    padding: 18px 22px 16px;
    border-bottom: 1px solid #111;
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.14em;
    color: #333;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 0;
    border-bottom: 1px solid #0E0E0E;
}

.stat-row:last-child { border-bottom: none; }

.stat-key {
    font-size: 12px;
    color: #444;
}

.stat-val {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #BDBDBD;
}

.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #22C55E;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2.4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.28; }
}

.sidebar-footer {
    padding: 14px 22px;
    border-top: 1px solid #111;
    margin-top: auto;
}

.footer-text {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #202020;
    letter-spacing: 0.06em;
}

/* ─── Topbar ─────────────────────────────── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 0 15px;
    border-bottom: 1px solid #141414;
    margin-bottom: 0;
}

.topbar-title {
    font-size: 14px;
    font-weight: 500;
    color: #FAFAFA;
    letter-spacing: -0.01em;
}

.topbar-badge {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #2E2E2E;
    letter-spacing: 0.06em;
}

/* ─── Welcome state ──────────────────────── */
.welcome-block {
    padding: 56px 0 40px;
}

.welcome-heading {
    font-size: 40px;
    font-weight: 600;
    color: #FAFAFA;
    letter-spacing: -0.04em;
    margin-bottom: 12px;
    line-height: 1.15;
}

.welcome-sub {
    font-size: 14px;
    color: #8E8E8E;
    line-height: 1.7;
    max-width: 480px;
    margin-bottom: 32px;
}

.topic-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    max-width: 500px;
}

.topic-chip {
    padding: 11px 16px;
    background: #080808;
    border: 1px solid #1C1C1C;
    border-radius: 4px;
    font-size: 12.5px;
    color: #8E8E8E;
    text-align: left;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s ease;
}

.topic-chip:hover {
    border-color: #3B82F6;
    color: #FAFAFA;
    background: #0E0E0E;
}

/* ─── Chat messages ──────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 16px 0 !important;
    margin: 0 !important;
    gap: 16px !important;
    box-shadow: none !important;
}

[data-testid="stChatMessage"] .stChatMessageContent {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* User bubble and layout */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stChatMessageContent {
    background: #0A0A0A !important;
    border: 1px solid #1E1E1E !important;
    border-right: 2px solid #3B82F6 !important;
    border-radius: 4px !important;
    padding: 12px 18px !important;
    max-width: 75% !important;
    display: block !important;
}

[data-testid="stChatMessage"] .stChatMessageContent p {
    font-size: 13px !important;
    line-height: 1.65 !important;
    color: #FAFAFA !important;
    margin: 0 !important;
}

/* Assistant text and layout */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stChatMessageContent p {
    color: #C0C0C0 !important;
    font-size: 13px !important;
    line-height: 1.72 !important;
}

/* Minimalist Avatar Styling (no colored background) */
[data-testid^="stChatMessageAvatar"] {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
}

[data-testid^="stChatMessageAvatar"] div {
    background-color: transparent !important;
    border: none !important;
    border-radius: 0 !important;
}

[data-testid^="stChatMessageAvatar"] img {
    border-radius: 0 !important;
    width: 32px !important;
    height: 32px !important;
    opacity: 0.85;
}

/* ─── Chat input ─────────────────────────── */
[data-testid="stChatInputContainer"] {
    padding: 20px 0 24px !important;
    border-top: 1px solid #141414 !important;
    background: #000 !important;
}

[data-testid="stChatInput"] {
    background: #0A0A0A !important;
    border: 1px solid #222222 !important;
    border-radius: 8px !important;
    min-height: 56px !important;
    padding: 0 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"]:hover {
    border-color: #333333 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6, 0 4px 20px rgba(59, 130, 246, 0.15) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #FAFAFA !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.55 !important;
    padding: 16px 20px !important;
    caret-color: #3B82F6 !important;
    min-height: 56px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #666666 !important;
}

/* Send button */
[data-testid="stChatInput"] button[kind="primaryFormSubmit"],
[data-testid="stChatInput"] button {
    background: transparent !important;
    border: none !important;
    border-left: 1px solid #222222 !important;
    border-radius: 0 7px 7px 0 !important;
    width: 56px !important;
    min-width: 56px !important;
    height: 100% !important;
    min-height: 56px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #8E8E8E !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] button:hover {
    background: #111111 !important;
    color: #3B82F6 !important;
}

[data-testid="stChatInput"] button svg {
    width: 18px !important;
    height: 18px !important;
    stroke-width: 2.0 !important;
}

/* ─── Spinner ────────────────────────────── */
.stSpinner > div {
    border-top-color: #222 !important;
}

/* ─── Hide Streamlit chrome ──────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ─── Scrollbar ──────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1A1A1A; border-radius: 2px; }

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-name">Lauki Phones</div>
        <div class="brand-tagline">Customer Support Console</div>
    </div>

    <div class="sidebar-section">
        <div class="section-label">Agent</div>
        <div class="stat-row">
            <span class="stat-key">Status</span>
            <span class="stat-val"><span class="status-dot"></span>Online</span>
        </div>
        <div class="stat-row">
            <span class="stat-key">Runtime</span>
            <span class="stat-val">AgentCore</span>
        </div>
        <div class="stat-row">
            <span class="stat-key">Memory</span>
            <span class="stat-val">Active</span>
        </div>
    </div>

    <div class="sidebar-footer">
        <div class="footer-text">v0.1.0 — internal</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Topbar
# -----------------------------
st.markdown("""
<div class="topbar">
    <span class="topbar-title">Customer Support Agent</span>
    <span class="topbar-badge">AWS AgentCore</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Chat State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Welcome State
# -----------------------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-block">
        <div class="welcome-heading">How can we help?</div>
        <div class="welcome-sub">
            Ask about your plan, SIM, billing, roaming, or account. The agent
            searches the Lauki knowledge base in real time.
        </div>
        <div class="topic-grid">
            <div class="topic-chip">SIM activation</div>
            <div class="topic-chip">Roaming services</div>
            <div class="topic-chip">Number porting</div>
            <div class="topic-chip">Billing &amp; invoices</div>
            <div class="topic-chip">Account security</div>
            <div class="topic-chip">Plans &amp; addons</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Chat History
# -----------------------------
for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask a question...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):

        with st.spinner(""):

            AGENTCORE_EXE = r"C:\Users\admin\Desktop\AgentCore\.venv\Scripts\agentcore.exe"

            response = None

            try:
                result = subprocess.run(
                    [
                        AGENTCORE_EXE,
                        "invoke",
                        json.dumps({"prompt": prompt})
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    env={
                        **os.environ,
                        "AGENTCORE_SUPPRESS_RECOMMENDATION": "1",
                        "PYTHONUTF8": "1"
                    },
                    timeout=30,
                )

                output = result.stdout

                if "Response:" in output:
                    response = output.split("Response:", 1)[1].strip()

                    # Remove traceback if present
                    if "Traceback" in response:
                        response = response.split("Traceback", 1)[0].strip()

                else:
                    response = "No response received from AgentCore."

            except Exception as e:
                response = f"Error: {str(e)}"

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})