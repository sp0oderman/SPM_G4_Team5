<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">SPM_G4_TEAM5</h1></p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/sp0oderman/SPM_G4_Team5?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/sp0oderman/SPM_G4_Team5?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/sp0oderman/SPM_G4_Team5?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/sp0oderman/SPM_G4_Team5?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>❯ REPLACE-ME</code>

---

##  Features

<code>❯ REPLACE-ME</code>

---

##  Project Structure

```sh
└── SPM_G4_Team5/
    ├── .github
    │   └── workflows
    │       └── ci.yml
    ├── Backend
    │   ├── __init__.py
    │   ├── app.py
    │   ├── config.py
    │   ├── requirements.txt
    │   ├── src
    │   │   ├── models
    │   │   │   ├── employees.py
    │   │   │   ├── wfh_requests.py
    │   │   │   └── withdrawal_requests.py
    │   │   ├── routes
    │   │   │   ├── employees_routes.py
    │   │   │   ├── wfh_requests_routes.py
    │   │   │   └── withdrawal_requests_routes.py
    │   │   ├── services
    │   │   │   ├── employees_services.py
    │   │   │   ├── wfh_requests_services.py
    │   │   │   └── withdrawal_requests_services.py
    │   │   └── utils
    │   │       └── email_functions.py
    │   ├── tests
    │   │   ├── integration_tests
    │   │   │   ├── test_employees.py
    │   │   │   ├── test_login.py
    │   │   │   ├── test_wfh_req_apply_approve_reject_withdraw.py
    │   │   │   ├── test_wfh_req_util.py
    │   │   │   ├── test_withdrawal_req_apply_approve_reject.py
    │   │   │   └── test_withdrawal_req_util.py
    │   │   └── unit_tests
    │   │       ├── test_employees_routes.py
    │   │       ├── test_employees_services.py
    │   │       ├── test_wfh_requests_routes.py
    │   │       ├── test_wfh_requests_services.py
    │   │       ├── test_withdrawal_requests_routes.py
    │   │       └── test_withdrawal_requests_services.py
    │   └── vercel.json
    ├── Frontend
    │   ├── .browserslistrc
    │   ├── .editorconfig
    │   ├── .eslintrc-auto-import.json
    │   ├── .eslintrc.js
    │   ├── README.md
    │   ├── index.html
    │   ├── jsconfig.json
    │   ├── package-lock.json
    │   ├── package.json
    │   ├── public
    │   │   └── favicon.ico
    │   ├── src
    │   │   ├── App.vue
    │   │   ├── assets
    │   │   │   ├── logo.png
    │   │   │   └── logo.svg
    │   │   ├── components
    │   │   │   ├── Alerts
    │   │   │   │   └── AlertMessage.vue
    │   │   │   ├── Buttons
    │   │   │   │   ├── Management
    │   │   │   │   └── Personal
    │   │   │   ├── MenuBars
    │   │   │   │   ├── CEOMenuBar.vue
    │   │   │   │   ├── HRMenuBar.vue
    │   │   │   │   ├── ManagerMenuBar.vue
    │   │   │   │   └── MenuBar.vue
    │   │   │   ├── README.md
    │   │   │   ├── Schedules
    │   │   │   │   ├── Legend.vue
    │   │   │   │   ├── ManagementCalendar.vue
    │   │   │   │   ├── MyTeamCalendar.vue
    │   │   │   │   ├── PersonalCalendar.vue
    │   │   │   │   └── SurbordinateCalendar.vue
    │   │   │   ├── WFHRequests
    │   │   │   │   ├── ApplyWFHPrompt.vue
    │   │   │   │   ├── ListWFHRequests.vue
    │   │   │   │   ├── PersonalListWFHRequests.vue
    │   │   │   │   ├── ViewWFHRequests.vue
    │   │   │   │   └── WFHRequests.vue
    │   │   │   └── WithdrawalRequests
    │   │   │       ├── ListWithdrawalRequests.vue
    │   │   │       ├── PersonalListWithdrawalRequests.vue
    │   │   │       ├── ViewWithdrawalRequests.vue
    │   │   │       ├── WithdrawWFHDialog.vue
    │   │   │       └── WithdrawalRequests.vue
    │   │   ├── layouts
    │   │   │   ├── README.md
    │   │   │   └── default.vue
    │   │   ├── main.js
    │   │   ├── pages
    │   │   │   ├── README.md
    │   │   │   ├── ceo
    │   │   │   │   ├── OverallSchedule.vue
    │   │   │   │   ├── SurbordinateSchedule.vue
    │   │   │   │   ├── TeamWFHRequests.vue
    │   │   │   │   └── TeamWithdrawalRequests.vue
    │   │   │   ├── hr
    │   │   │   │   ├── OverallSchedule.vue
    │   │   │   │   ├── PersonalSchedule.vue
    │   │   │   │   ├── PersonalWFHRequests.vue
    │   │   │   │   ├── PersonalWithdrawalRequests.vue
    │   │   │   │   └── TeamSchedule.vue
    │   │   │   ├── index.vue
    │   │   │   ├── manager
    │   │   │   │   ├── ColleagueSchedule.vue
    │   │   │   │   ├── OverallSchedule.vue
    │   │   │   │   ├── PersonalSchedule.vue
    │   │   │   │   ├── PersonalWFHRequests.vue
    │   │   │   │   ├── PersonalWithdrawalRequests.vue
    │   │   │   │   ├── SurbordinateSchedule.vue
    │   │   │   │   ├── TeamWFHRequests.vue
    │   │   │   │   └── TeamWithdrawalRequests.vue
    │   │   │   └── staff
    │   │   │       ├── PersonalSchedule.vue
    │   │   │       ├── PersonalWFHRequests.vue
    │   │   │       ├── PersonalWithdrawalRequests.vue
    │   │   │       └── TeamSchedule.vue
    │   │   ├── plugins
    │   │   │   ├── README.md
    │   │   │   ├── index.js
    │   │   │   └── vuetify.js
    │   │   ├── router
    │   │   │   └── index.js
    │   │   ├── stores
    │   │   │   ├── README.md
    │   │   │   ├── auth.js
    │   │   │   └── index.js
    │   │   └── styles
    │   │       ├── README.md
    │   │       └── settings.scss
    │   ├── vercel.json
    │   └── vite.config.mjs
    └── README.md
```


###  Project Index
<details open>
	<summary><b><code>SPM_G4_TEAM5/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			</table>
		</blockquote>
	</details>
	<details> <!-- .github Submodule -->
		<summary><b>.github</b></summary>
		<blockquote>
			<details>
				<summary><b>workflows</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/.github/workflows/ci.yml'>ci.yml</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- Frontend Submodule -->
		<summary><b>Frontend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/.eslintrc-auto-import.json'>.eslintrc-auto-import.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/package-lock.json'>package-lock.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/vite.config.mjs'>vite.config.mjs</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/vercel.json'>vercel.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/.browserslistrc'>.browserslistrc</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/jsconfig.json'>jsconfig.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/package.json'>package.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/.eslintrc.js'>.eslintrc.js</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/index.html'>index.html</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>src</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/main.js'>main.js</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/App.vue'>App.vue</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
					<details>
						<summary><b>layouts</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/layouts/default.vue'>default.vue</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>styles</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/styles/settings.scss'>settings.scss</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>components</b></summary>
						<blockquote>
							<details>
								<summary><b>Alerts</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Alerts/AlertMessage.vue'>AlertMessage.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>Buttons</b></summary>
								<blockquote>
									<details>
										<summary><b>Management</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Management/MyTeamWFH.vue'>MyTeamWFH.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Management/MyTeamSchedule.vue'>MyTeamSchedule.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Management/ButtonContainer.vue'>ButtonContainer.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Management/MyTeamWithdraw.vue'>MyTeamWithdraw.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>Personal</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Personal/MyWFHRequests.vue'>MyWFHRequests.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Personal/MySchedule.vue'>MySchedule.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Personal/PersonalButtonContainer.vue'>PersonalButtonContainer.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Buttons/Personal/MyWithdrawalRequests.vue'>MyWithdrawalRequests.vue</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>WFHRequests</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WFHRequests/WFHRequests.vue'>WFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WFHRequests/ViewWFHRequests.vue'>ViewWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WFHRequests/ListWFHRequests.vue'>ListWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WFHRequests/PersonalListWFHRequests.vue'>PersonalListWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WFHRequests/ApplyWFHPrompt.vue'>ApplyWFHPrompt.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>MenuBars</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/MenuBars/MenuBar.vue'>MenuBar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/MenuBars/HRMenuBar.vue'>HRMenuBar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/MenuBars/CEOMenuBar.vue'>CEOMenuBar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/MenuBars/ManagerMenuBar.vue'>ManagerMenuBar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>Schedules</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Schedules/ManagementCalendar.vue'>ManagementCalendar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Schedules/PersonalCalendar.vue'>PersonalCalendar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Schedules/SurbordinateCalendar.vue'>SurbordinateCalendar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Schedules/Legend.vue'>Legend.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/Schedules/MyTeamCalendar.vue'>MyTeamCalendar.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>WithdrawalRequests</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WithdrawalRequests/ListWithdrawalRequests.vue'>ListWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WithdrawalRequests/PersonalListWithdrawalRequests.vue'>PersonalListWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WithdrawalRequests/WithdrawalRequests.vue'>WithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WithdrawalRequests/ViewWithdrawalRequests.vue'>ViewWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/components/WithdrawalRequests/WithdrawWFHDialog.vue'>WithdrawWFHDialog.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>pages</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/index.vue'>index.vue</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>manager</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/TeamWithdrawalRequests.vue'>TeamWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/SurbordinateSchedule.vue'>SurbordinateSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/OverallSchedule.vue'>OverallSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/PersonalWithdrawalRequests.vue'>PersonalWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/TeamWFHRequests.vue'>TeamWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/PersonalSchedule.vue'>PersonalSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/ColleagueSchedule.vue'>ColleagueSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/manager/PersonalWFHRequests.vue'>PersonalWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>ceo</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/ceo/TeamWithdrawalRequests.vue'>TeamWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/ceo/SurbordinateSchedule.vue'>SurbordinateSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/ceo/OverallSchedule.vue'>OverallSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/ceo/TeamWFHRequests.vue'>TeamWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>hr</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/hr/TeamSchedule.vue'>TeamSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/hr/OverallSchedule.vue'>OverallSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/hr/PersonalWithdrawalRequests.vue'>PersonalWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/hr/PersonalSchedule.vue'>PersonalSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/hr/PersonalWFHRequests.vue'>PersonalWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>staff</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/staff/TeamSchedule.vue'>TeamSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/staff/PersonalWithdrawalRequests.vue'>PersonalWithdrawalRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/staff/PersonalSchedule.vue'>PersonalSchedule.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/pages/staff/PersonalWFHRequests.vue'>PersonalWFHRequests.vue</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>plugins</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/plugins/vuetify.js'>vuetify.js</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/plugins/index.js'>index.js</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>router</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/router/index.js'>index.js</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>stores</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/stores/index.js'>index.js</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Frontend/src/stores/auth.js'>auth.js</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- Backend Submodule -->
		<summary><b>Backend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/vercel.json'>vercel.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/app.py'>app.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/config.py'>config.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>src</b></summary>
				<blockquote>
					<details>
						<summary><b>models</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/models/wfh_requests.py'>wfh_requests.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/models/withdrawal_requests.py'>withdrawal_requests.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/models/employees.py'>employees.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>routes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/routes/wfh_requests_routes.py'>wfh_requests_routes.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/routes/employees_routes.py'>employees_routes.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/routes/withdrawal_requests_routes.py'>withdrawal_requests_routes.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>utils</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/utils/email_functions.py'>email_functions.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>services</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/services/withdrawal_requests_services.py'>withdrawal_requests_services.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/services/wfh_requests_services.py'>wfh_requests_services.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/services/employees_services.py'>employees_services.py</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with SPM_G4_Team5, ensure your runtime environment meets the following requirements:

- **Programming Language:** Vue.js
- **Package Manager:** Npm, Pip


###  Installation

Install SPM_G4_Team5 using one of the following methods:

**Build from source:**

1. Clone the SPM_G4_Team5 repository:
```sh
❯ git clone https://github.com/sp0oderman/SPM_G4_Team5
```

2. Navigate to the project directory:
```sh
❯ cd SPM_G4_Team5
```

3. Install the project dependencies:


**Using `npm`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-INSTALL-COMMAND-HERE'
```


**Using `pip`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-INSTALL-COMMAND-HERE'
```




###  Usage
Run SPM_G4_Team5 using the following command:
**Using `npm`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-RUN-COMMAND-HERE'
```


**Using `pip`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-RUN-COMMAND-HERE'
```


###  Testing
Run the test suite using the following command:
**Using `npm`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-TEST-COMMAND-HERE'
```


**Using `pip`** &nbsp; [<img align="center" src="" />]()

```sh
❯ echo 'INSERT-TEST-COMMAND-HERE'
```


---
##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/sp0oderman/SPM_G4_Team5/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/sp0oderman/SPM_G4_Team5/issues)**: Submit bugs found or log feature requests for the `SPM_G4_Team5` project.
- **💡 [Submit Pull Requests](https://github.com/sp0oderman/SPM_G4_Team5/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/sp0oderman/SPM_G4_Team5
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/sp0oderman/SPM_G4_Team5/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=sp0oderman/SPM_G4_Team5">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
