# SOAP and related HTTP shapes

Bruno does not use a separate `meta.type` for SOAP. Model SOAP as **`type: http`** with XML body and SOAPAction / Content-Type headers.

## SOAP over HTTP

Prefer **WSDL import** in Bruno when a `.wsdl` exists (generates operations and envelopes). For hand-authored collections:

```bru
meta {
  name: GetAccount
  type: http
  seq: 1
}

post {
  url: {{soapEndpoint}}
  body: xml
  auth: basic
}

auth:basic {
  username: {{username}}
  password: {{password}}
}

headers {
  Content-Type: text/xml; charset=utf-8
  SOAPAction: "urn:GetAccount"
}

body:xml {
  <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
      <GetAccount xmlns="urn:example">
        <AccountId>{{accountId}}</AccountId>
      </GetAccount>
    </soap:Body>
  </soap:Envelope>
}

docs {
  SOAP GetAccount operation.

  ## Success
  - **200** — SOAP body with `GetAccountResponse`

  ## Errors
  - **500** — SOAP Fault; document `faultcode`, `faultstring`, detail elements
}
```

Environment: `soapEndpoint` (often same host as legacy XML gateway). Chained IDs use the same `bru.setEnvVar` pattern after parsing XML in `script:post-response` if needed (prefer documenting manual copy for fragile XPath).

## SSE

Server-Sent Events are normal HTTP requests with `Accept: text/event-stream`. See the SSE section in `references/protocols/rest-http.md`.
