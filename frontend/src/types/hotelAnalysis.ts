export interface HotelAnalysisRequest {
  reviews: string[];
  preferences?: {
    travel_style?: string;
    priority?: string;
    non_negotiable?: string;
    persona?: string;
    analysis_key?: string;
  };
}

export interface HotelAnalysisResponse {
  // 1-5 score fields (numeric, normalized)
  cleaning_score: number;
  quietness_score: number;
  service_score: number;
  location_score: number;
  wifi_score: number;
  breakfast_score: number;
  family_friendly_score: number;
  entertainment_score: number;
  room_comfort_score: number;
  value_for_money_score: number;

  // Still useful for the UI detail line
  has_playground: boolean;
  pros: string[];
  cons: string[];
}
