import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export async function getCampaigns() {
  const { data, error } = await supabase
    .from('campaigns')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data || [];
}

export async function getCreatives(campaignId = null) {
  let query = supabase
    .from('creatives')
    .select('*')
    .order('created_at', { ascending: false });

  if (campaignId) {
    query = query.eq('campaign_id', campaignId);
  }

  const { data, error } = await query;

  if (error) throw error;
  return data || [];
}

export async function getApprovalEvents(creativeId) {
  const { data, error } = await supabase
    .from('approval_events')
    .select('*')
    .eq('creative_id', creativeId)
    .order('created_at', { ascending: true });

  if (error) throw error;
  return data || [];
}

export async function getTraffickingRecords(creativeId = null) {
  let query = supabase
    .from('trafficking_records')
    .select('*')
    .order('created_at', { ascending: false });

  if (creativeId) {
    query = query.eq('creative_id', creativeId);
  }

  const { data, error } = await query;

  if (error) throw error;
  return data || [];
}

export async function getSupplyPaths() {
  const { data, error } = await supabase
    .from('supply_paths')
    .select('*');

  if (error) throw error;
  return data || [];
}

export async function getDSPSpecs() {
  const { data, error } = await supabase
    .from('dsp_specs')
    .select('*');

  if (error) throw error;
  return data || [];
}
