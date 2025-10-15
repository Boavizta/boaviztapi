workspace "SIG - Green Cloud Practices" "The Green Cloud Practices system represents a web application used by clients to intuitively visualise and improve the sustainability and costs of their computing instances, be it on premiseor in the cloud." {

    !identifiers hierarchical

    model {
        # Start of Context Diagram
        buser = person "Business User" "A regular business user"
        suser = person "Specialised User" "A domain expert user"

        gcpSystem = softwareSystem "SIG - Green Cloud Practices System" "Allows clients to calculate their computing costs and emissions, compare cloud providers and reduce cloud spending." {
            tags "Internal System"
            webDashboard = container "Single-Page Application" "Provides all of the dashboarding functionality to the clients via their web browser" "Next.js and React" {
                tags "Web Application" "Internal System"
            }
            backendAPI = container "API Application" "Provides sustainability impact and electricity costs via JSON/HTTPS API" "Python and FastAPI" {
                tags "Internal System"
                electricityPricesRouter = component "Electricity Prices Router" "Allows user to query electricity prices" "FastAPI APIRouter" {
                    tags "Internal Component"
                }
                costsProviderService = component "Electricity Costs Provider Service" "Provides functions to query real-time electricity prices from heterogeneous sources" "Python Script" {
                   tags "Internal Component"
                }
                cloudRouter = component "Cloud Router" "Allows users to query sustainability impacts and operating costs for cloud instances" "FastAPI APIRouter" {
                    tags "Internal Component"
                }
                impactsComputationService = component "Impacts Computation Service" "Calculates the sustainability impacts of on-premise hardware and cloud instances" "Python Script" {
                    tags "Internal Component"
                }
                serverRouter = component "Server Router" "Allows users to query sustainability impacts and operating costs for on-premise hardware" "FastAPI APIRouter" {
                    tags "Internal Component"
                }
            }

        }

        cacheSystem = softwareSystem "Cache" "Caches the most used and computationally expensive data such as external API responses" "Redis Cache" {
            tags "Cache"
        }
        fileSystem = softwareSystem "File System" "CSV/YAML/JSON Files from multiple sources including scrapers" {
            tags "File System"
        }
        vantageSystem = softwareSystem "Vantage Cloud Provider Comparison API" "Allows clients to compare instances offered by multiple cloud providers" {
            tags "External System"
        }
        electricityMapsSystem = softwareSystem "ElectricityMaps API" "Allows clients to compare electricity sources (fossils vs hydro) in real time" {
            tags "External System"
        }
        boaviztaSystem = softwareSystem "Boavizta Sustainability Impacts System" "Open-source API allowing clients to compute sustainability impacts" {
            tags "External System"
        }
        ENTSOESystem = softwareSystem "European Network of Transmission System Operators ENTSO-E" "European system used to gather electricity-related data such as day-ahead prices" {
            tags "External System"
        }

        gcpSystem -> vantageSystem "Gets cloud instance information using"
        gcpSystem -> electricityMapsSystem "Gets electricity source breakdown information using"
        gcpSystem -> boaviztaSystem "Builds upon the foundation set by" "Github Fork"
        gcpSystem -> ENTSOESystem "Gathers real-time electricity prices using"

        # End of Context Diagram

        # Start of Container Diagram

        buser -> gcpSystem.webDashboard "Views reports, compares emissions and costs using"
        suser -> gcpSystem.webDashboard "Computes reports, creates portfolios of instances using"

        gcpSystem.webDashboard -> gcpSystem.backendAPI "Makes API calls to" "JSON/HTTPS"

        gcpSystem.backendAPI -> ENTSOESystem "Makes API Calls to" "XML/HTTPS"
        gcpSystem.backendAPI -> vantageSystem "Scrapes data from"
        gcpSystem.backendAPI -> electricityMapsSystem "Makes API Calls to" "JSON/HTTPS"
        gcpSystem.backendAPI -> boaviztaSystem "Uses static data from" "CSV files"

        # End of Container Diagram

        # Start of Component Diagram

        gcpSystem.backendAPI.costsProviderService -> cacheSystem "Fetches cached data" "redis-py client"
        gcpSystem.backendAPI.costsProviderService -> ENTSOESystem "Makes API calls to" "JSON/HTTPS"

        gcpSystem.backendAPI.impactsComputationService -> fileSystem "Uses stored data from" "CSV/YAML/JSON"

        gcpSystem.backendAPI.electricityPricesRouter -> gcpSystem.backendAPI.costsProviderService "Uses"
        gcpSystem.backendAPI.cloudRouter -> gcpSystem.backendAPI.impactsComputationService "Uses"
        gcpSystem.backendAPI.serverRouter -> gcpSystem.backendAPI.impactsComputationService "Uses"


        gcpSystem.webDashboard -> gcpSystem.backendAPI.electricityPricesRouter "Makes API calls to" "JSON/HTTPS"
        gcpSystem.webDashboard -> gcpSystem.backendAPI.cloudRouter "Makes API calls to" "JSON/HTTPS"
        gcpSystem.webDashboard -> gcpSystem.backendAPI.serverRouter "Makes API calls to" "JSON/HTTPS"

        # End of Component diagram
    }

    views {
        systemContext gcpSystem "Context" "System Context Diagram for the SIG Green Cloud Practices application" {
            include *
            exclude cacheSystem
            exclude fileSystem
            autolayout lr
        }

        container gcpSystem "GCPContainerDiagram" "Container Diagram for the SIG Green Cloud Practices system" {
            include *
            exclude cacheSystem
            exclude fileSystem
            autolayout lr
        }

        component gcpSystem.backendAPI "BackendAPIComponentDiagram" "Component Diagram for the backend API used by the SIG Green Cloud Practices web application" {
            include *
            autolayout lr
        }

        styles {
            element "External System" {
                background #919092
                stroke #919092
                color #000000
                shape RoundedBox
            }
            element "Internal System" {
                background #2e6bff
                stroke #2e6bff
                color #ffffff
                shape RoundedBox
            }
            element "Internal Component" {
                background #638aff
                stroke #638aff
                color #ffffff
                shape RoundedBox
            }
            element "Web Application" {
                shape WebBrowser
            }
            element "Person" {
                shape person
                color #ffffff
                background #00297a
            }
            element "Database" {
                shape cylinder
                color #ffffff
                background #2e6bff
            }
            element "Cache" {
                shape cylinder
                color #ffffff
                background #2e6bff
            }
            element "File System" {
                shape folder
                background #FFE9A2
                color #000000
            }
            element "Boundary" {
                strokeWidth 5
            }
            relationship "Relationship" {
                thickness 4
            }
        }
    }

    configuration {
        scope softwaresystem
    }

}