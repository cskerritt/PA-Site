// The Railway project "PA-Site" as Infrastructure as Code: the one service this repository
// deploys (pa-expert-site, purintonanalytics.com) with its source, build, deploy and domain
// settings. The Railway CLI evaluates this file and diffs it against the LIVE environment
// (there is no state file): `railway config plan` shows the differences, `railway config
// apply` makes the environment match. It replaces the deprecated railway.json config-as-code
// file, which Railway stops reading on 2026-12-01.
//
// No behaviour change: every value below is what the service runs with TODAY. The build and
// deploy blocks are the values railway.json applied on every deploy (they were never stored
// on the service, so `railway config pull` could not see them); source, replicas and domains
// are exactly what `railway config pull` rendered from the live service on 2026-10-03.
//
// This file is a NAMED PARTIAL: it owns only the resources it declares (pa-expert-site) and
// leaves anything else in the environment alone, so it can never delete something it does
// not know about. The first apply claims ownership of service.pa-expert-site.
//
// Variables: the service has none today (variables/PA-Site__pa-expert-site.txt is empty), so
// there is no env block. If a variable is ever added in the dashboard, list it here as
// `preserve()` (import it from "railway/iac") so a later apply keeps it rather than removing
// it; never put a literal secret in this file.
import { defineRailway, github, project, service } from "railway/iac";

export const partial = "pa-site";

export default defineRailway(() =>
  project("PA-Site", {
    resources: [
      service("pa-expert-site", {
        // Live source (pull): GitHub cskerritt/PA-Site, branch main, no root directory,
        // "wait for CI" off.
        source: github("cskerritt/PA-Site", { branch: "main", checkSuites: false }),
        // From railway.json (file-only until now): the root Dockerfile (python build stage,
        // then Caddy serving the generated site on $PORT, default 8080).
        build: { builder: "DOCKERFILE", dockerfilePath: "Dockerfile" },
        // From railway.json (file-only until now): GET / must answer within 60 s before a new
        // deployment takes traffic; restart on failure up to 5 times. The stored service value
        // is Railway's default (ON_FAILURE, 10 retries), so only the retry count is declared to
        // pin the file's 5. Railway reports a default as unset, so the policy type (ON_FAILURE, the default) is not declared - declaring it never converges (verified 2026-10-03); only the non-default retry count is.
        deploy: {
          healthcheckPath: "/",
          healthcheckTimeout: 60,
          restartPolicyMaxRetries: 5,
        },
        // Live placement (pull): one replica in us-east4 (Virginia).
        replicas: { "us-east4-eqdc4a": 1 },
        // Live custom domain (pull). It targets port 8080 on Railway; pull renders it without
        // the port and plans clean that way. The generated pa-expert-site-production.up.railway.app
        // domain is never declared ("Generated Railway service domains are not included").
        domains: ["purintonanalytics.com"],
      }),
    ],
  }),
);
