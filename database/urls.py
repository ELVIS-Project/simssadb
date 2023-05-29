from django.urls import path
from django.contrib.auth import views as auth_views
from database.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("search/", SearchView.as_view(), name="search"),
    path("archives/<int:pk>", ArchiveDetailView.as_view(), name="archive-detail"),
    path("archives/", ArchiveListView.as_view(), name="archive-list"),
    path("create/", CreationView.as_view(), name="create"),
    path(
        "contributions/",
        ContributionMusicalWorkListView.as_view(),
        name="contributionmusicalwork-list",
    ),
    path(
        "contributions/<int:pk>",
        ContributionMusicalWorkListView.as_view(),
        name="contributionmusicalwork-detail",
    ),
    path(
        "encodingworkflows/",
        EncodingWorkflowListView.as_view(),
        name="encodingworkflows-list",
    ),
    path(
        "encodingworkflows/<int:pk>",
        EncodingWorkflowDetailView.as_view(),
        name="encodingworkflow-detail",
    ),
    path(
        "experimentalstudies",
        ExperimentalStudyListView.as_view(),
        name="experimentalstudy-list",
    ),
    path(
        "experimentalstudies/<int:pk>",
        ExperimentalStudyDetailView.as_view(),
        name="experimentalstudy-detail",
    ),
    path(
        "extractedfeatures",
        ExtractedFeatureListView.as_view(),
        name="extractedfeature-list",
    ),
    path(
        "extractedfeatures/<int:pk>",
        ExtractedFeatureDetailView.as_view(),
        name="extractedfeature-detail",
    ),
    path("featurefiles/", FeatureFileListView.as_view(), name="featurefile-list"),
    path(
        "featurefiles/<int:pk>",
        FeatureFileDetailView.as_view(),
        name="featurefile-detail",
    ),
    path("featuretypes/", FeatureTypeListView.as_view(), name="featuretype-list"),
    path(
        "featuretypes/<int:pk>",
        FeatureTypeListView.as_view(),
        name="featuretype-detail",
    ),
    path(
        "file-create/", FileCreationView.as_view(), name="file-creation", #testing
    ),
    path("files/", FileListView.as_view(), name="file-list"),
    path("files/<int:pk>", FileDetailView.as_view(), name="file-detail"),
    path("styles/", GenreAsInStyleListView.as_view(), name="genreasinstyle-detail"),
    path(
        "styles/<int:pk>",
        GenreAsInStyleDetailView.as_view(),
        name="genreasinstyle-detail",
    ),
    path("types/", GenreAsInTypeListView.as_view(), name="genreasintype-list"),
    path(
        "types/<int:pk>", GenreAsInTypeDetailView.as_view(), name="genreasintype-detail"
    ),
    path("areas/", GeographicAreaListView.as_view(), name="geographicarea-list"),
    path(
        "areas/<int:pk>",
        GeographicAreaDetailView.as_view(),
        name="geographicarea-detail",
    ),
    path("instruments/", InstrumentListView.as_view(), name="instrument-list"),
    path(
        "instruments/<int:pk>", InstrumentDetailView.as_view(), name="instrument-detail"
    ),
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("languages/<int:pk>", LanguageDetailView.as_view(), name="language-detail"),
    path(
        "musicalworks/<int:pk>",
        MusicalWorkDetailView.as_view(),
        name="musicalwork-detail",
    ),
    path("musicalworks/", MusicalWorkListView.as_view(), name="musicalwork-list"),
    path("parts/", PartListView.as_view(), name="part-list"),
    path("parts/<int:pk>", PartDetailView.as_view(), name="part-detail"),
    path("persons/<int:pk>", PersonDetailView.as_view(), name="person-detail"),
    path("persons/", PersonListView.as_view(), name="person-list"),
    path(
        "researchcorpora/", ResearchCorpusListView.as_view(), name="researchcorpus-list"
    ),
    path(
        "researchcorpora/<int:pk>",
        ResearchCorpusDetailView.as_view(),
        name="researchcorpus-detail",
    ),
    path("sections/", SectionListView.as_view(), name="section-list"),
    path("sections/<int:pk>", SectionDetailView.as_view(), name="section-detail"),
    path("softwares/", SoftwareListView.as_view(), name="software-list"),
    path("softwares/<int:pk>", SoftwareDetailView.as_view(), name="software-detail"),
    path("sources/", SourceListView.as_view(), name="source-list"),
    path("sources/<int:pk>", SourceDetailView.as_view(), name="source-detail"),
    path("typesofsection/", TypeOfSectionListView.as_view(), name="typeofsection-list"),
    path(
        "typesofsection/<int:pk>",
        TypeOfSectionDetailView.as_view(),
        name="typeofsection-detail",
    ),
    path(
        "validationworkflows/",
        ValidationWorkFlowListView.as_view(),
        name="validationworkflow-list",
    ),
    path(
        "validationworkflows/<int:pk>",
        ValidationWorkFlowDetailView.as_view(),
        name="validationworkflow-detail",
    ),
    path("download/content/<int:pk>", download_content_file, name="download-content"),
    path("download/feature/<int:pk>", download_feature_file, name="download-feature"),
    path("download/cart/", download_cart, name="download-cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("ajax/add_to_cart/", add_to_cart, name="add-to-cart"),
    path("ajax/remove_from_cart/", remove_from_cart, name="remove-from-cart"),
    path("ajax/clear_cart/", clear_cart, name="clear-cart"),
    # from create view
    path("musical-work-create/", CreateMusicalWorkViewCustom.as_view(), name="musical-work-creation"), # testing
    path("research-corpus-create/", CreateResearchCorpus.as_view(), name="research-corpus-creation"), # testing

    # autocomplete views
    path("type-autocomplete/", TypeAutocomplete.as_view(), name="type-autocomplete"),
    path("file-autocomplete/", FileAutocomplete.as_view(), name="file-autocomplete"),
    path('instrument-autcomplete/', InstrumentAutocomplete.as_view(), name='instrument-autocomplete'),
    path('geographicarea-autocomplete/', GeographicAreaAutocomplete.as_view(), name='geographicarea-autocomplete'),
    path('software-autocomplete/', SoftwareAutocomplete.as_view(), name='software-autocomplete'),
    path('archive-autocomplete/', ArchiveAutocomplete.as_view(), name='archive-autocomplete'),
    path('style-autocomplete/', StyleAutocomplete.as_view(), name='style-autocomplete'),
]
