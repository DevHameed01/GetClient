import { useState } from 'react'
import type { FormEvent } from 'react'

export function FindLeads() {
  const [industry, setIndustry] = useState('')
  const [location, setLocation] = useState('')
  const [companySize, setCompanySize] = useState('')
  const [keywords, setKeywords] = useState('')
  const [searchAttempted, setSearchAttempted] = useState(false)

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSearchAttempted(true)
  }

  return (
    <section className="find-leads-page" aria-label="Find leads">
      <div className="find-leads-intro">
        <p className="eyebrow">Lead discovery</p>
        <h3>Find businesses that fit your goals.</h3>
        <p>Set your search criteria to focus on the businesses you want to reach.</p>
      </div>

      <form className="panel lead-search-form" onSubmit={handleSearch}>
        <div className="lead-search-heading">
          <div>
            <p className="eyebrow">Search criteria</p>
            <h3>Define your ideal businesses</h3>
          </div>
          <span>Refine your search with any combination of filters.</span>
        </div>

        <div className="lead-search-fields">
          <label>
            Industry
            <input
              type="text"
              name="industry"
              value={industry}
              onChange={(event) => setIndustry(event.target.value)}
              placeholder="e.g. Hospitality"
              autoComplete="off"
            />
          </label>

          <label>
            Location
            <input
              type="text"
              name="location"
              value={location}
              onChange={(event) => setLocation(event.target.value)}
              placeholder="City, region, or country"
              autoComplete="off"
            />
          </label>

          <label>
            Company size
            <select
              name="companySize"
              value={companySize}
              onChange={(event) => setCompanySize(event.target.value)}
            >
              <option value="">Any company size</option>
              <option value="1-10">1–10 employees</option>
              <option value="11-50">11–50 employees</option>
              <option value="51-200">51–200 employees</option>
              <option value="201-500">201–500 employees</option>
              <option value="501+">501+ employees</option>
            </select>
          </label>

          <label className="lead-keyword-field">
            Keywords
            <input
              type="search"
              name="keywords"
              value={keywords}
              onChange={(event) => setKeywords(event.target.value)}
              placeholder="Add services, characteristics, or terms"
              autoComplete="off"
            />
          </label>
        </div>

        <div className="lead-search-actions">
          <p>Discovery is not connected yet. Searches will not fetch or create business records.</p>
          <button type="submit" className="primary-button">Search businesses</button>
        </div>
      </form>

      <section className="panel lead-results" aria-labelledby="lead-results-heading" aria-live="polite">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Results</p>
            <h3 id="lead-results-heading">Businesses</h3>
          </div>
        </div>
        <div className="lead-results-empty">
          <span className="lead-results-icon" aria-hidden="true">⌕</span>
          <h4>{searchAttempted ? 'No search results available' : 'Your search results will appear here'}</h4>
          <p>
            {searchAttempted
              ? 'Lead discovery is not connected yet, so no search was sent and no business results were fetched.'
              : 'Add any search criteria above. Business discovery will be available here when it is implemented.'}
          </p>
        </div>
      </section>
    </section>
  )
}
