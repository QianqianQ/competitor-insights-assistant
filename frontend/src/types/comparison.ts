export interface BusinessCoreAttributes {
  name: string;
  website?: string | null;
  address?: string | null;
  rating?: number | null;
  rating_count?: number | null;
  image_count?: number | null;
  category?: string | null; // 'type' in backend BusinessProfile model
  has_hours?: boolean | null;
  has_description?: boolean | null;
  has_menu_link?: boolean | null;
  has_price_level?: boolean | null;
  latitude?: number | null;
  longitude?: number | null;
}

// This will represent the structure of user_business and each item in competitors
export interface DisplayBusinessProfile extends BusinessCoreAttributes {
  identifier_used?: string; // The input string for user, or name for competitor
  profile_data_source?: string; // e.g., "mock" or "serper.dev"
  // Frontend calculated score
  profile_score?: number;
  // Frontend calculated rank
  rank?: number;
}

export interface ComparisonReportData {
  report_id?: string;
  user_business: DisplayBusinessProfile;
  competitor_businesses: DisplayBusinessProfile[];
  ai_comparison_summary: string;
  ai_improvement_suggestions: string[];
  metadata?: {
    llm_provider?: string;
    llm_model?: string;
    tokens_used?: number;
  };
  created_at?: string;
}

export interface ComparisonRequestPayload {
  user_business_identifier: string;
  report_style?: 'casual' | 'data-driven';
}

// For the Pinia store state
export interface ComparisonState {
  isLoading: boolean;
  error: string | null;
  report: ComparisonReportData | null;
  userInput: string; // To store the user_business_identifier input
  isNavigating: boolean; // To track navigation state
}