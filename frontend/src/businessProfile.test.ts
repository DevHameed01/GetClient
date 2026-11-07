import { afterEach, describe, expect, it, vi } from 'vitest'
import { updateBusinessProfile } from './businessProfile'

describe('updateBusinessProfile', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('sends only editable fields in the PUT request', async () => {
    const profile = {
      id: 'profile-123',
      created_at: '2026-01-01T00:00:00Z',
      updated_at: '2026-01-02T00:00:00Z',
      business_name: 'Example Co',
      description: 'An example business',
      industry: 'Technology',
      website: 'https://example.com/',
      location: 'Remote',
      products_and_services: 'Consulting',
      target_market: 'Small businesses',
      unique_value_proposition: 'Personal service',
      communication_style: 'Professional',
    }
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(profile), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    )

    await updateBusinessProfile(profile, 'org-123')

    const [url, request] = vi.mocked(fetch).mock.calls[0]
    expect(url).toBe('/api/business-profile')
    expect(request?.method).toBe('PUT')
    expect(JSON.parse(String(request?.body))).toEqual({
      business_name: 'Example Co',
      description: 'An example business',
      industry: 'Technology',
      website: 'https://example.com/',
      location: 'Remote',
      products_and_services: 'Consulting',
      target_market: 'Small businesses',
      unique_value_proposition: 'Personal service',
      communication_style: 'Professional',
    })
  })
})
