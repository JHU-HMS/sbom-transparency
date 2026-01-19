# The SBOM Transparency v. Exposure Dilemma: A Case Study on Adversarial Access to Public SBOMs in Healthcare

Repository for the paper by Jiarou Deng, Yang Yang (Johns Hopkins University), and Michael Rushanan (Harbor Labs).

This repo contains code and artifacts to reproduce the study's analyses of public software bills of materials (SBOMs) in healthcare and their impact.

## Table of Contents

- [Whats in this Repo](#whats-in-this-repo)
- [Quickstart](#quickstart)
- [Reproducing Results](#reproducing-results)
- [Artifacts](#artifacts)
- [Citation](#citation)
- [Contributions](#contributions)
- [Responsible Use](#responsible-use)
- [License](#license)
- [Contact](#contact)

## Whats in this Repo

Health and Medical Security (HMS) lab research projects organize tools and data with implications beyond the research paper in their own top-level directories. The artifacts directory includes code and data relevant to the paper and reproducibility of the research. The paper directory contains the camera-ready LaTeX clone, written in Overleaf.

```
├── deidentify/        # SBOM anonymization script
├── sboms/             # Case-study SBOMs (sources noted in README in this dir)
├── artifacts/         # Reproduction steps, intermediate outputs, figures
│   ├── scripts/       # Dependency Track container to perform SBOM CVE lookup
│   ├── analysis/      # CVE exploit validation containers and logs
└── paper/             # LaTeX source for the manuscript
```

## Quickstart

We performed our analysis on Kali Linux. Any Debian-based Linux distribution should work similarly; however, we cannot warrant the results. All commands are executed in a terminal emulator and in the `./artifacts` directory. 

### 1. Install Software Tools and Dependencies

```bash
$ sudo apt install docker.io docker-compose python3
```

### 2. Build Dependency Track Container

```bash
$ cd ./cve-lookup 
$ docker compose up -d --build
```
### 3. Export Dependency Track API Key

1. Go to [http://localhost:8080/](http://localhost:8080/)
2. Log in using the default credentials `admin`/`admin`
3. Navigate to `Administration/Access Management/Team`
4. Select `Automation`
5. In `Permissions`, select: `PORTFOLIO_MANAGEMENT`, `PROJECT_CREATION_UPLOAD`, and `VIEW_PORTFOLIO `
6. Select `API Keys` and generate an API key
7. Copy the key to use it as an environment variable

### 4. Export DT_API_KEY in Dependency Track

```bash
$ # In ./cve-lookup directory
$ docker exec -it python-client bash
$ export DT_API_KEY=your_api_key_here
```

### 5. Execute Dependency Track Scan on an SBOM

```bash
$ # In ./cve-lookup directory
$ python owasp_scan.py
```

### 6. Access Scan Results

The `vuln_list.json` file is generated using the Dependency Track API after it performs a complete vulnerability lookup on the de-identified SBOM software component CPEs and PURLs using default vulnerability sources, including GitHub Advisories, NVD, and OSV data. Our code filters vulnerabilities by Critical and High severity to minimize the size of our target data set.

```bash
$ # In ./cve-lookup directory
$ cat vuln_list.json
```

### 7. Semi-Automated Analysis using LLMs

We implemented a semi-automated analysis using the OpenAI o3 model. In particular, we entered a structured prompt into the ChatGPT chat interface for each CVE we identified in our previous steps, then recorded the model-generated step-by-step attack procedure or *blueprint*, as we call it. We captured the attack blueprints in the `./artifacts` directory.

The following list enumerates our semi-automated analysis in detail:

1. Export CVEs from Dependency Track (`vuln_list.json`)
2. For each CVE, craft a structured prompt (`./artifacts/analysis/prompt.txt`) that includes the CVE ID
3. Enter the prompt into the ChatGPT chat interface and record the model-generated step-by-step attack blueprint.
4. Implement the model’s suggested exploitation steps in a controlled Docker container to validate the exploit (i.e., did it work or not)
4. If a suggested step fails, copy the error message (or failing output) back into the chat and request targeted debugging guidance
5. Iterate with the model until the step succeeds or problems are unresolved
6. Record the final, validated steps

While we used ChatGPT and the OpenAI o3 model, our approach is not limited to these technologies.

## Reproducing Results

This section details how to utilize the provided inputs to replicate our reported outputs, a step that is crucial for the integrity and reproducibility of the research.

### Steps

1. Browse to [ChatGPT](https://chatgpt.com)
2. Optionally, though recommended, log in using your personal account
3. Start a new chat
4. Select `o3` in the model selector
5. Open the file `./artifacts/analysis/prompt.txt`
6. Copy all of its contents and enter the CVE-ID of your choice
7. Paste the content and CVE-ID into ChatGPT as your message
8. Send the message without adding anything else
9. (Optional) Save the full reply as `./artifacts/analysis/response.txt`

### Notes

Do not enable browsing/tools or add extra instructions. Using the exact prompt text and o3 model is sufficient for reproducing our reported output.

## Artifacts

We captured our artifacts in the `./artifacts` directory. Important files and folders include:

1. `./artifacts/scripts`
2. `./artifacts/analysis`

## Citation

```bibtex
@inproceedings{deng-yang-rushanan-healthsec25,
  author    = {Jiarou Deng and Yang Yang and Michael Rushanan},
  title     = {The SBOM Transparency v. Exposure Dilemma: A Case Study on Adversarial Access to Public SBOMs in Healthcare},
  booktitle = {Proceedings of the Healthcare Security Workshop (HealthSec 2025)},
  note      = {ACSAC Workshop},
  location  = {Honolulu, Hawaii, USA},
  date      = {2025-12-09},
  year      = {2025},
  publisher = {IEEE},
  url       = {https://publish.illinois.edu/healthsec2025/}
}
```

## Contributions

We welcome contributions that:

* Improve automation of SBOM attack blueprints
* Validate proof-of-concept exploits in a controlled research setting
* Enhance de-identification and evaluation metrics

Please open an issue first to discuss the scope of a contribution. For code, submit a PR that references the issue, includes tests, a short design note, and, where applicable, before/after results. See [GitHub Issues](https://docs.github.com/en/issues) for more information, or [Link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) to get started now.

## Responsible Use

* **Research use only:** This repository and its associated exploit validation code should be for research only. 
* **Healthcare context:** Be mindful of how you use the deidentification tool, as anonymized SBOMs may still reveal sensitive vendor or product composition details. 
* **Disclosure:** If you discover a previously unreported vulnerability, follow the coordinated disclosure process for the software or product in question, and do not file the details here.

## License

See [LICENSE.md](./LICENSE.md).

## Contact

Please contact [Dr. Michael Rushanan](https://github.com/micharu123), the principal investigator, for any reason not described above.
