<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">SPM_G4_TEAM5</h1></p>
<p align="center">
	<em><code>❯ WFH Management System</code></em>
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

## Deployment

<b>You can access the live application here:</b> [Click Me!!!](https://spm-g4-team5.vercel.app/)

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

---

##  Overview

A <b>role-based</b> WFH management system that allows staff to <b>apply, modify, and withdraw WFH requests</b>, while providing managers, directors, and HR with <b>visibility and control over team and department schedules</b>.

---

##  Features

### Human Resources and Senior Management
- **View Overall and Team Schedules**: 
	- Access an overview of all teams' schedules.
- **Staff Location Overview**: 
	- See count of staff members working from the office or remotely, sorted by team.

### Managers and Directors
- **View Team Schedule**: 
	- View the schedules of team members within their own team.
- **Approve or Reject Arrangements**: 
	- Review, Approve, or Reject WFH requests. 
	- View a list of pending requests.
- **Withdraw Arrangements**: 
	- Manage approved WFH requests, with the option to withdraw specific ones.

### Staff
- **View Team Schedule**: 
	- View the schedules of team members within their own team.
- **View Own Schedule**: 
	- Access a personal schedule to stay updated on own WFH requests.
- **Apply for Flexible Working Arrangement**: 
	- Submit requests for new flexible working arrangements.
- **Withdraw Arrangement**: 
	- Withdraw an approved or pending WFH request.
</code>

---

##  Project Structure

``` sh
	SPM_G4_Team5
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
	│   │   ├── routes
	│   │   ├── services
	│   │   └── utils
	│   └── tests
	│       ├── integration_tests
	│       └── unit_tests
	└── Frontend
		└── src
			├── components
			│   ├── Alerts
			│   ├── Buttons
			│   ├── MenuBars
			│   ├── Schedules
			│   ├── WFHRequests
			│   └── WithdrawalRequests
			└── pages
				├── ceo
				├── hr
				├── manager
				└── staff
```

###  Project Index
<details open>
	<summary><b><code>SPM_G4_TEAM5/</code></b></summary>
	<details> <!-- .github Submodule -->
		<summary><b>.github</b></summary>
		<blockquote>
			<details>
				<summary><b>workflows</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/.github/workflows/ci.yml'>ci.yml</a></b></td>
						<td><code>❯ Configure CI using GitHub Actions</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- Frontend Submodule -->
		<summary><b>Frontend</b></summary>
		<blockquote>
			<details>
				<summary><b>src</b></summary>
				<blockquote>
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
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- Backend Submodule -->
		<summary><b>Backend</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/app.py'>app.py</a></b></td>
				<td><code>❯ Entry point of Backend Application</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/config.py'>config.py</a></b></td>
				<td><code>❯ Configuration file of Backend Application</code></td>
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
								<td><code>❯ ORM for wfh_requests table</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/models/withdrawal_requests.py'>withdrawal_requests.py</a></b></td>
								<td><code>❯ ORM for withdrawal_requests table</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/models/employees.py'>employees.py</a></b></td>
								<td><code>❯ ORM for employees table</code></td>
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
								<td><code>❯ Controller for routes pertaining to WFH Requests</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/routes/employees_routes.py'>employees_routes.py</a></b></td>
								<td><code>❯ Controller for routes pertaining to Employees</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/routes/withdrawal_requests_routes.py'>withdrawal_requests_routes.py</a></b></td>
								<td><code>❯ Controller for routes pertaining to Withdrawal Requests</code></td>
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
								<td><code>❯ Functions pertaining to sending Emails</code></td>
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
								<td><code>❯ Services pertaining to Withdrawal Requests</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/services/wfh_requests_services.py'>wfh_requests_services.py</a></b></td>
								<td><code>❯ Services pertaining to WFH Requests</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/sp0oderman/SPM_G4_Team5/blob/master/Backend/src/services/employees_services.py'>employees_services.py</a></b></td>
								<td><code>❯ Services pertaining to Employees</code></td>
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

Install the Application using the following method:

1. Clone the SPM_G4_Team5 repository:

```sh
git clone https://github.com/sp0oderman/SPM_G4_Team5
```

2. Navigate to the <b>Backend</b> of the project directory:

```sh
cd SPM_G4_Team5/Backend
```

3. Install the project <b>Backend</b> dependencies:

```sh
run 'pip install -r requirements.txt' in the terminal
```

4. Navigate to the <b>Frontend</b> of the project directory:

```sh
cd SPM_G4_Team5/Frontend
```

5. Install the project <b>Frontend</b> dependencies:

```sh
run 'npm install' in the terminal
```

###  Usage

<b>Before running</b> the application, <b>set up the following environment variables:</b>

| Variable Name        | Description                          | Example Value                            |
|----------------------|--------------------------------------|------------------------------------------|
| `DB_URI`             | Database connection URL              | `postgresql://user:pass@localhost/dbname`|
| `SECRET_KEY`         | Secret key for application config    | `your-secret-key`                        |
| `EMAIL_ACCOUNT`      | Gmail Account to send Emails         | `name@gmail.com`                         |
| `EMAIL_PASSWORD`     | Gmail Account App Password           | `your_gmail_app_password`                |

To set these variables use the commands below (Or you can use a .env file):
- **On Windows:** Use `set` command, e.g., `set DB_URI=your_database_url`
- **On MacOS/Linux:** Use `export` command, e.g., `export DB_URI=your_database_url`

---

Run the Application using the following commands (A separate terminal required for Frontend and Backend):

1. In one terminal, navigate to the <b>Backend</b> of the project directory:

```sh
cd SPM_G4_Team5/Backend
```

2. Run the <b>Backend</b> application:

```sh
run 'python app.py' in the terminal
```

3. In another terminal, navigate to the <b>Frontend</b> of the project directory:

```sh
cd SPM_G4_Team5/Frontend
```

4. Run the <b>Frontend</b> application:

```sh
run 'npm run dev' in the terminal
```


###  Testing
Run the test suite using the following command:

1. Navigate to the <b>Backend</b> of the project directory:

```sh
cd SPM_G4_Team5/Backend
```

2. To run <b>unit test</b> suite:

```sh
run 'python -m unittest discover -s tests/unit_tests' in the terminal
```

3. To run <b>integration test</b> suite:

```sh
run 'python -m unittest discover -s tests/integration_tests' in the terminal
```

---
