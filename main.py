"""Compatibility entry point for running the packaged application locally."""

from ai_gemini_test.app import (
    ConstructionSeriesAnalysis,
    ImageAnalysis,
    ResourceComparison,
    ResourceStateChange,
    SafetyAssessment,
    SiteResources,
    analysis_view,
    analyze_image,
    analyze_image_series,
    analyze_series_for_publication,
    analyze_uploaded_image,
    analyze_uploaded_series,
    build_app,
    clear_results,
    clear_series_results,
    clear_series_workspace,
    format_label,
    format_list,
    load_env_file,
    main,
    publish_series_report,
)

__all__ = [
    "ConstructionSeriesAnalysis",
    "ImageAnalysis",
    "ResourceComparison",
    "ResourceStateChange",
    "SafetyAssessment",
    "SiteResources",
    "analysis_view",
    "analyze_image",
    "analyze_image_series",
    "analyze_series_for_publication",
    "analyze_uploaded_image",
    "analyze_uploaded_series",
    "build_app",
    "clear_results",
    "clear_series_results",
    "clear_series_workspace",
    "format_label",
    "format_list",
    "load_env_file",
    "main",
    "publish_series_report",
]


if __name__ == "__main__":
    main()
