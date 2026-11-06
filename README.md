# Wazuh-Ransomware-Mitigation
Automated Ransomware Detection and Mitigation using Wazuh SIEM Active Response

# Automated Ransomware Detection and Mitigation with Wazuh SIEM

## 📌 Project Overview
This project demonstrates the implementation of an automated detection and active response system to contain ransomware attacks in real-time using **Wazuh SIEM/EDR**. The laboratory simulates a real-world enterprise cyber threat scenario where an attacker compromises a server and executes file-encrypting malware, triggering automated firewall containment policies within seconds.

### 🛡️ Laboratory Architecture
* **SIEM / Victim Server:** Ubuntu Server (running Wazuh Manager & hosting critical enterprise files)
* **Attacker Host:** Parrot OS / Kali Linux (simulating remote exploitation over SSH)

---

## 🛠️ Phase 1: Environment & FIM Monitoring
The victim server contains a critical directory located at `/home/wilf/datos_criticos`. Wazuh's **File Integrity Monitoring (FIM)** module was configured to watch this folder in real-time by adding the following block to `/var/ossec/etc/ossec.conf`:

```xml
<directories realtime="yes" check_all="yes">/home/wilf/datos_criticos</directories>
```

---

## ☣️ Phase 2: Attack Simulation (Ransomware)
A Python script (`ransomware.py`) utilizing robust symmetric encryption (`cryptography` library) was executed remotely via SSH from the attacker's machine. The malware performs the following actions:
1. Iterates over the critical data directory.
2. Encrypts files using the Fernet algorithm, appending a `.locked` extension.
3. Deletes original unencrypted files.
4. Drops a ransom note (`RESCATE.txt`).

---

## 🎯 Phase 3: Detection Engineering & Active Response
To stop the threat before total data destruction, a custom Wazuh rule was engineered in `local_rules.xml` to detect the massive creation of `.locked` files:

```xml
<group name="local,syscheck,">
  <rule id="100002" level="12">
    <if_matched_sid>554</if_matched_sid> <!-- Native file added rule -->
    <match>.locked</match>
    <description>Critical Alert: Ransomware behavior detected in data directory.</description>
  </rule>
</group>
```

An **Active Response** policy was linked to this specific rule inside `ossec.conf` to automatically trigger the native `firewall-drop` script, isolating the attacker's IP for 10 minutes:

```xml
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>100002</rules_id>
  <timeout>600</timeout>
</active-response>
```

---

## 📊 Phase 4: Results & Visual Proof
When the ransomware script was launched from the Parrot OS machine, it managed to encrypt the first few files. However, within milliseconds, Wazuh identified the pattern, triggered **Rule 100002**, and immediately executed the firewall drop policy. 

The attacker's SSH terminal froze instantly, containing the threat and preventing full system compromise.

### 🚀 Proof of Mitigation (Wazuh Dashboard)
*Include your Wazuh dashboard screenshot showing rules 554, 100002, 553, and 651 here*

---

## 🔄 Phase 5: Incident Recovery (Post-Incident)
Once the threat actor was successfully banned by the firewall, a recovery script (`decrypt.py`) was executed on the local server to restore the few files encrypted before containment, using the symmetric key saved securely during the environment simulation.

---

## 🧠 Key Takeaways & Skills Demonstrated
* **SIEM/EDR Engineering:** Advanced Wazuh rule creation and configuration (`ossec.conf`).
* **Incident Response (IR):** Setting up automated containment playbooks to reduce Mean Time to Remediation (MTTR).
* **Malware Simulation:** Understanding ransomware mechanics, indicators of compromise (IoCs), and encryption flows.
