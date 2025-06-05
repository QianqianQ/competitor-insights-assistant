export interface ComparisonRequestPayload {
  user_business_identifier: string;
  report_style?: 'casual' | 'data-driven';
}

export interface ComparisonReportData {
  user_business: DisplayBusinessProfile;
  competitor_businesses: DisplayBusinessProfile[];
  competitor_count: number;
  ai_comparison_summary: string;
  ai_improvement_suggestions: string[];
  metadata?: {
    llm_provider?: string;
    llm_model?: string;
    tokens_used?: number;
  };
  report_id?: string;
  created_at?: string;
}

export interface DisplayBusinessProfile {
  name: string;
  website?: string | null;
  address?: string | null;
  rating?: number | null;
  rating_count?: number | null;
  image_count?: number | null;
  category?: string | null;
  has_hours?: boolean | null;
  has_description?: boolean | null;
  has_menu_link?: boolean | null;
  has_price_level?: boolean | null;
  latitude?: number | null;
  longitude?: number | null;
  // Frontend calculated score
  profile_score?: number;
  rank?: number;
}

// For the Pinia store state
export interface ComparisonState {
  isLoading: boolean;
  error: string | null;
  report: ComparisonReportData | null;
  userInput: string; // To store the user_business_identifier input
  isNavigating: boolean; // To track navigation state
}
