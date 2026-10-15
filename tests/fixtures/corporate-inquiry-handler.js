// Contract fixture copied from bb369tech/bb369-sendgrid-api server.js
// Source main at read time: 2dfe3d86b0c2d0d7a0990706b894077fcf762fc1
// Network and email are mocked in tests; this file does not start a server.
app.post(
  "/api/corporate-inquiry",
  async (req, res) => {
    try {
      const {
        name,
        company,
        email,
        country,
        inquiryType,
        message,
        privacyConsent
      } = req.body || {};

      if (
        !name ||
        !email ||
        !inquiryType ||
        !message ||
        privacyConsent !==
          "accepted"
      ) {
        return res.status(400).json({
          success: false,
          message:
            "Please complete all required fields."
        });
      }

      const safeName =
        String(name)
          .trim()
          .slice(0, 100);

      const safeCompany =
        String(company || "")
          .trim()
          .slice(0, 150);

      const safeEmail =
        String(email)
          .trim()
          .toLowerCase()
          .slice(0, 200);

      const safeCountry =
        String(country || "")
          .trim()
          .slice(0, 100);

      const safeInquiryType =
        String(inquiryType)
          .trim()
          .slice(0, 100);

      const safeMessage =
        String(message)
          .trim()
          .slice(0, 3000);

      const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (
        !emailPattern.test(
          safeEmail
        )
      ) {
        return res.status(400).json({
          success: false,
          message:
            "Please enter a valid email address."
        });
      }

      const internalHtml = `
        <div style="
          font-family:Arial,sans-serif;
          line-height:1.65;
          color:#111827;
        ">
          <h2>
            New BB369TECH Corporate Inquiry
          </h2>

          <p>
            <strong>Source:</strong>
            BB369TECH Corporate Website
          </p>

          <p>
            <strong>Website:</strong>
            <a href="https://bb369tech.com">
              https://bb369tech.com
            </a>
          </p>

          <hr style="
            border:0;
            border-top:1px solid #e5e7eb;
            margin:22px 0;
          ">

          <p>
            <strong>Name:</strong>
            ${escapeHtml(
              safeName
            )}
          </p>

          <p>
            <strong>Company:</strong>
            ${escapeHtml(
              safeCompany ||
              "Not provided"
            )}
          </p>

          <p>
            <strong>Email:</strong>
            ${escapeHtml(
              safeEmail
            )}
          </p>

          <p>
            <strong>Country / Region:</strong>
            ${escapeHtml(
              safeCountry ||
              "Not provided"
            )}
          </p>

          <p>
            <strong>Inquiry Type:</strong>
            ${escapeHtml(
              safeInquiryType
            )}
          </p>

          <p>
            <strong>Message:</strong>
          </p>

          <div style="
            background:#f6f7f9;
            padding:14px;
            border-radius:8px;
            white-space:pre-wrap;
          ">
            ${escapeHtml(
              safeMessage
            )}
          </div>
        </div>
      `;

      const customerHtml = `
        <div style="
          font-family:Arial,sans-serif;
          line-height:1.65;
          color:#111827;
        ">
          <h2>
            We Received Your Inquiry
          </h2>

          <p>
            Hello ${escapeHtml(
              safeName
            )},
          </p>

          <p>
            Thank you for contacting BB369TECH.
            Your inquiry has been received by
            our corporate team.
          </p>

          <p>
            We will review the information and
            respond through the contact details
            you provided when appropriate.
          </p>

          <p>
            This confirmation does not create a
            contract, partnership, service
            commitment, or guaranteed response
            time.
          </p>

          <p>
            BB369TECH<br>
            Los Angeles, California,
            United States<br>

            <a href="https://bb369tech.com">
              https://bb369tech.com
            </a>
          </p>
        </div>
      `;

      await sgMail.send({
        to: CORPORATE_TO_EMAIL,
        from: FROM_EMAIL,
        replyTo: safeEmail,

        subject:
          `[Corporate Inquiry] ` +
          `${safeInquiryType} - ` +
          `${safeName}`,

        html: internalHtml
      });

      await sgMail.send({
        to: safeEmail,
        from: FROM_EMAIL,

        replyTo:
          CORPORATE_TO_EMAIL,

        subject:
          "BB369TECH Received Your Inquiry",

        html: customerHtml
      });

      return res.status(200).json({
        success: true,
        message:
          "Your inquiry has been received."
      });
    } catch (err) {
      console.error(
        "Corporate inquiry submission error:",
        err.response?.body ||
        err
      );

      return res.status(500).json({
        success: false,
        message:
          "Unable to submit the inquiry at this time."
      });
    }
  }
);

