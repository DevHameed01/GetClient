import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'
import './Auth.css'
import { apiRequest, ApiError } from './api'
import { updateBusinessProfile } from './businessProfile'
import type { BusinessProfileInput } from './businessProfile'

type AuthMode = 'login' | 'register'
type Organization = { id: string; name: string; role: string }

const emptyProfile: BusinessProfileInput = {
  business_name: '',
  description: '',
  industry: '',
  website: '',
  location: '',
  products_and_services: '',
  target_market: '',
  unique_value_proposition: '',
  communication_style: 'Professional',
}

const profileFields: { name: keyof BusinessProfileInput; label: string; multiline?: boolean }[] = [
  { name: 'business_name', label: 'Business name' },
  { name: 'description', label: 'Business description', multiline: true },
  { name: 'industry', label: 'Industry' },
  { name: 'website', label: 'Website' },
  { name: 'location', label: 'Location' },
  { name: 'products_and_services', label: 'Products and services', multiline: true },
  { name: 'target_market', label: 'Target market', multiline: true },
  { name: 'unique_value_proposition', label: 'Unique value proposition', multiline: true },
  { name: 'communication_style', label: 'Preferred communication style' },
]

function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : 'Something went wrong. Please try again.'
}

function App() {
  const [authMode, setAuthMode] = useState<AuthMode>('login')
  const [authenticated, setAuthenticated] = useState(false)
  const [checkingSession, setCheckingSession] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [organizationName, setOrganizationName] = useState('')
  const [organizations, setOrganizations] = useState<Organization[]>([])
  const [selectedOrganizationId, setSelectedOrganizationId] = useState('')
  const [workspaceName, setWorkspaceName] = useState('')
  const [profile, setProfile] = useState<BusinessProfileInput>(emptyProfile)
  const [profileExists, setProfileExists] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  async function loadProfile(organizationId: string) {
    try {
      const savedProfile = await apiRequest<BusinessProfileInput>('/business-profile', {}, organizationId)
      setProfile(savedProfile)
      setProfileExists(true)
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 404) {
        setProfile(emptyProfile)
        setProfileExists(false)
        return
      }
      throw requestError
    }
  }

  async function loadOrganizations() {
    const available = await apiRequest<Organization[]>('/organizations')
    setOrganizations(available)
    const storedId = window.localStorage.getItem('getclient-active-organization')
    const selected = available.find((organization) => organization.id === storedId) ?? available[0]
    if (!selected) {
      setError('Your account does not have an organisation workspace yet.')
      return
    }
    setSelectedOrganizationId(selected.id)
    setWorkspaceName(selected.name)
    window.localStorage.setItem('getclient-active-organization', selected.id)
    await loadProfile(selected.id)
  }

  useEffect(() => {
    let active = true
    void apiRequest('/auth/session')
      .then(() => apiRequest<Organization[]>('/organizations'))
      .then(async (available) => {
        if (!active) return
        setOrganizations(available)
        const storedId = window.localStorage.getItem('getclient-active-organization')
        const selected = available.find((organization) => organization.id === storedId) ?? available[0]
        if (selected) {
          setSelectedOrganizationId(selected.id)
          setWorkspaceName(selected.name)
          window.localStorage.setItem('getclient-active-organization', selected.id)
          await loadProfile(selected.id)
        }
        if (active) setAuthenticated(true)
      })
      .catch(() => {
        if (active) setAuthenticated(false)
      })
      .finally(() => {
        if (active) setCheckingSession(false)
      })
    return () => {
      active = false
    }
  }, [])

  async function handleAuthSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    setNotice('')
    try {
      const path = authMode === 'register' ? '/auth/register' : '/auth/login'
      const body = authMode === 'register'
        ? { email, password, organization_name: organizationName }
        : { email, password }
      await apiRequest(path, { method: 'POST', body: JSON.stringify(body) })
      await loadOrganizations()
      setAuthenticated(true)
    } catch (requestError) {
      setError(errorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  async function selectOrganization(organizationId: string) {
    const selected = organizations.find((organization) => organization.id === organizationId)
    if (!selected) return
    setSelectedOrganizationId(selected.id)
    setWorkspaceName(selected.name)
    window.localStorage.setItem('getclient-active-organization', selected.id)
    setError('')
    setNotice('')
    try {
      await loadProfile(selected.id)
    } catch (requestError) {
      setError(errorMessage(requestError))
    }
  }

  async function saveOrganization(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedOrganizationId) return
    setError('')
    setNotice('')
    try {
      const updated = await apiRequest<Organization>(
        '/organization',
        { method: 'PATCH', body: JSON.stringify({ name: workspaceName }) },
        selectedOrganizationId,
      )
      setWorkspaceName(updated.name)
      setOrganizations((current) => current.map((item) => item.id === updated.id ? updated : item))
      setNotice('Workspace name saved.')
    } catch (requestError) {
      setError(errorMessage(requestError))
    }
  }

  async function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedOrganizationId) return
    setError('')
    setNotice('')
    try {
      const saved = await updateBusinessProfile(profile, selectedOrganizationId)
      setProfile(saved)
      setProfileExists(true)
      setNotice('Business profile saved.')
    } catch (requestError) {
      setError(errorMessage(requestError))
    }
  }

  async function logout() {
    try {
      await apiRequest('/auth/logout', { method: 'POST' })
    } catch {
      setError('Could not reach the server. Your session may still be active.')
    } finally {
      setAuthenticated(false)
      setOrganizations([])
      setSelectedOrganizationId('')
      setProfile(emptyProfile)
      setProfileExists(false)
      setPassword('')
      setNotice('')
    }
  }

  if (checkingSession) {
    return <main className="session-check" aria-live="polite">Checking your session…</main>
  }

  if (!authenticated) {
    return (
      <main className="auth-layout">
        <section className="auth-intro">
          <div className="brand-block">
            <div className="brand-mark">G</div>
            <div>
              <p className="eyebrow">AI prospecting</p>
              <h1>GetClient</h1>
            </div>
          </div>
          <div className="auth-copy">
            <p className="eyebrow">Better client conversations start here</p>
            <h2>Find the right clients. Start better conversations.</h2>
            <p>Keep your business context and prospecting work together in one workspace.</p>
          </div>
          <span className="auth-index">01 / Workspace access</span>
        </section>

        <section className="auth-panel" aria-labelledby="auth-title">
          <div className="auth-tabs" role="tablist" aria-label="Account access">
            <button type="button" role="tab" aria-selected={authMode === 'login'} onClick={() => setAuthMode('login')}>
              Sign in
            </button>
            <button type="button" role="tab" aria-selected={authMode === 'register'} onClick={() => setAuthMode('register')}>
              Create account
            </button>
          </div>
          <div className="auth-heading">
            <p className="eyebrow">{authMode === 'register' ? 'Get started' : 'Welcome back'}</p>
            <h2 id="auth-title">{authMode === 'register' ? 'Create your workspace' : 'Sign in to GetClient'}</h2>
          </div>
          <form className="auth-form" onSubmit={handleAuthSubmit}>
            {authMode === 'register' && (
              <label>
                Workspace name
                <input value={organizationName} onChange={(event) => setOrganizationName(event.target.value)} required maxLength={200} autoComplete="organization" />
              </label>
            )}
            <label>
              Email address
              <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required autoComplete="email" />
            </label>
            <label>
              Password
              <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required minLength={authMode === 'register' ? 12 : 1} maxLength={128} autoComplete={authMode === 'register' ? 'new-password' : 'current-password'} />
            </label>
            {error && <p className="form-message error-message" role="alert">{error}</p>}
            <button type="submit" className="primary-button auth-submit" disabled={submitting}>
              {submitting ? 'Please wait…' : authMode === 'register' ? 'Create workspace' : 'Sign in'}
            </button>
          </form>
        </section>
      </main>
    )
  }

  const selectedRole = organizations.find((organization) => organization.id === selectedOrganizationId)?.role

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">G</div>
          <div>
            <p className="eyebrow">AI prospecting</p>
            <h1>GetClient</h1>
          </div>
        </div>
        <div className="workspace-switcher">
          <label className="eyebrow" htmlFor="workspace-select">Workspace</label>
          <select id="workspace-select" value={selectedOrganizationId} onChange={(event) => void selectOrganization(event.target.value)}>
            {organizations.map((organization) => <option key={organization.id} value={organization.id}>{organization.name}</option>)}
          </select>
          {selectedRole && <span className="role-label">{selectedRole}</span>}
        </div>
        <div className="sidebar-note">
          <span className="status-dot" />
          <span>Workspace data is private to its members.</span>
        </div>
        <button type="button" className="nav-item logout-button" onClick={() => void logout()}>Sign out</button>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Workspace setup</p>
            <h2>Business profile</h2>
          </div>
          <span className="profile-status">{profileExists ? 'Profile configured' : 'Setup in progress'}</span>
        </header>

        {error && <p className="form-message error-message page-message" role="alert">{error}</p>}
        {notice && <p className="form-message success-message page-message" role="status">{notice}</p>}

        <section className="settings-grid">
          <article className="panel workspace-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Organisation</p>
                <h3>Workspace details</h3>
              </div>
            </div>
            <form className="workspace-form" onSubmit={saveOrganization}>
              <label htmlFor="workspace-name">Workspace name</label>
              <div className="inline-form-row">
                <input id="workspace-name" value={workspaceName} onChange={(event) => setWorkspaceName(event.target.value)} required maxLength={200} />
                <button type="submit" className="secondary-button" disabled={selectedRole === 'member'}>Save name</button>
              </div>
            </form>
          </article>

          <article className="panel profile-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Business context</p>
                <h3>Tell us what you offer</h3>
              </div>
              <span className="required-note">All fields required</span>
            </div>
            <form className="profile-form" onSubmit={saveProfile}>
              {profileFields.map((field) => (
                <label key={field.name} className={field.multiline ? 'wide-field' : ''}>
                  {field.label}
                  {field.multiline ? (
                    <textarea
                      value={profile[field.name]}
                      onChange={(event) => setProfile((current) => ({ ...current, [field.name]: event.target.value }))}
                      required
                      rows={3}
                    />
                  ) : (
                    <input
                      type={field.name === 'website' ? 'url' : 'text'}
                      value={profile[field.name]}
                      onChange={(event) => setProfile((current) => ({ ...current, [field.name]: event.target.value }))}
                      required
                      maxLength={field.name === 'website' ? 2048 : undefined}
                    />
                  )}
                </label>
              ))}
              <div className="profile-actions wide-field">
                <span>Changes are saved to the selected workspace.</span>
                <button type="submit" className="primary-button">Save business profile</button>
              </div>
            </form>
          </article>
        </section>
      </main>
    </div>
  )
}

export default App
