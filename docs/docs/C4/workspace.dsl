workspace "SIG - Green Cloud Practices" "The Green Cloud Practices system represents a web application used by clients to intuitively visualise and improve the sustainability and costs of their computing instances." {

    !identifiers hierarchical

    model {
        # =========================================================
        # PEOPLE & MAIN SYSTEMS
        # =========================================================
        buser = person "Business User" "A regular business user"
        suser = person "Specialised User" "A domain expert user"

        gcpSystem = softwareSystem "SIG - Green Cloud Practices System" "Allows clients to calculate their computing costs and emissions, compare cloud providers and reduce cloud spending." {
            tags "Internal System"
            webDashboard = container "Single-Page Application" "Provides all of the dashboarding functionality to the clients via their web browser" "Next.js and React" {
                tags "Web Application"
            }
            backendAPI = container "API Application" "Provides sustainability impact and electricity costs via JSON/HTTPS API" "Python and FastAPI" {
                tags "Internal System"

                group "Routers" {
                    electricityRouter = component "Electricity Router" "Allows user to query electricity prices, power breakdowns and available countries" "FastAPI APIRouter" {
                        tags "Internal Component"
                    }
                    authRouter = component "Authentication Router" "Provides authentication tooling for identity providers (Google)" {
                        tags "Internal Component"
                    }
                    optionsRouter = component "Options Router" "Provides endpoints for the dropdown field values in the dashboard forms" {
                        tags "Internal Component"
                    }
                    configurationRouter = component "Configuration Router" "Provides CRUD endpoints for cloud and on-premise configurations" {
                        tags "Internal Component"
                    }
                    portfolioRouter = component "Portfolio Router" "Provides CRUD endpoints for portofolios of configurations" {
                        tags "Internal Component"
                    }
                    userRouter = component "User Router" "Provides user-scoped endpoints for retrieving configurations and portfolios" {
                        tags "Internal Component"
                    }
                    sustainabilityRouter = component "Sustainability Router" "Provides sustainability impact estimations for on-premise and cloud configurations" {
                        tags "Internal Component"
                    }
                    costsRouter = component "Costs Router" "Provides cost estimations for the electricity and usage of configurations" {
                        tags "Internal Component"
                    }
                }

                group "Services" {
                    costsProviderService = component "Electricity Costs Provider Service" "Provides functions to query real-time electricity prices from heterogeneous sources" "Python Script" {
                       tags "Internal Component"
                    }
                    carbonIntensityProvider = component "Power Breakdown Provider Service" "Interface for retrieving the power breakdown results from ElectricityMaps API" {
                        tags "Internal Component"
                    }
                    sustainabilityProvider = component "Sustainability Computation Service" "Calculates the sustainability impacts of on-premise hardware and cloud instances" "Python Script" {
                        tags "Internal Component"
                    }
                    googleAuthService = component "Google Authentication Service" "Backend handler for the Google Identity Service API" {
                        tags "Internal Component"
                    }
                    cloudProvider = component "Cloud Instance Provider" "Provides all the supported cloud instances and providers" {
                        tags "Internal Component"
                    }
                    utilsProvider = component "Utility Services Provider" "Utility API for interacting with data stored in the CSV files" {
                        tags "Internal Component"
                    }
                    configurationService = component "Configuration Service" "API Service layer for interacting with configuration models in the database" {
                        tags "Internal Component"
                    }
                    portfolioService = component "Portfolio Service" "API Service layer for interacting with portfolio models in the database" {
                        tags "Internal Component"
                    }
                    cacheService = component "Cache Service" "Caching service used for caching external API calls" {
                        tags "Internal Component"
                    }
                }
            }
        }

        cache = softwareSystem "Cache System" "Caching layer using MongoDB" {
            cacheSystem =  container "Cache" "Caches the most used and computationally expensive data such as external API responses" "MongoDB" {
                tags "Cache"
                scheduler = component "Scheduler" {
                    tags "Internal Component"
                }
            }
            tags "Internal System"
        }

        databaseSystem = softwareSystem "Database" "MongoDB Database" "MongoDB" {
            tags "Database"
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
        googleIdentityProviderSystem = softwareSystem "Google Identity Provider" "Offers OAuth2 Authentication/Authorization functionality" {
            tags "External System"
        }
        boaviztaSystem = softwareSystem "Boavizta Sustainability Impacts System" "Open-source API allowing clients to compute sustainability impacts" {
            tags "External System"
        }

        # =========================================================
        # RELATIONSHIPS
        # =========================================================
        gcpSystem -> vantageSystem "Gets cloud instance information using"
        gcpSystem -> electricityMapsSystem "Gets electricity source breakdown and pricing information using"
        gcpSystem -> boaviztaSystem "Builds upon the foundation set by" "Github Fork"
        gcpSystem -> googleIdentityProviderSystem "Authenticates users using"

        buser -> gcpSystem.webDashboard "Compares sustainability impacts and cost breakdowns using"
        suser -> gcpSystem.webDashboard "Computes reports, creates portfolios of configurations using"

        gcpSystem.webDashboard -> gcpSystem.backendAPI "Makes API calls to" "JSON/HTTPS"

        gcpSystem.backendAPI -> vantageSystem "Scrapes data from"
        gcpSystem.backendAPI -> electricityMapsSystem "Makes API Calls to" "JSON/HTTPS"
        gcpSystem.backendAPI -> boaviztaSystem "Uses static data from" "CSV files"

        gcpSystem.backendAPI.costsProviderService -> cache.cacheSystem "Fetches cached data" "redis-py client"
        gcpSystem.backendAPI.costsProviderService -> electricityMapsSystem "Makes API calls to" "JSON/HTTPS"

        gcpSystem.backendAPI.sustainabilityProvider -> fileSystem "Uses stored data from" "CSV/YAML/JSON"

        gcpSystem.backendAPI.electricityRouter -> gcpSystem.backendAPI.costsProviderService "Computes electricity costs"
        gcpSystem.backendAPI.electricityRouter -> gcpSystem.backendAPI.carbonIntensityProvider "Computes power breakdown"

        gcpSystem.backendAPI.authRouter -> gcpSystem.backendAPI.googleAuthService "OAuth2 using"

        gcpSystem.backendAPI.optionsRouter -> gcpSystem.backendAPI.cloudProvider "Gets Cloud instances"
        gcpSystem.backendAPI.optionsRouter -> gcpSystem.backendAPI.utilsProvider "Gets CSV Data"

        gcpSystem.backendAPI.configurationRouter -> gcpSystem.backendAPI.configurationService "Database Access Layer"

        gcpSystem.backendAPI.portfolioRouter -> gcpSystem.backendAPI.portfolioService "Database Access Layer"

        gcpSystem.backendAPI.userRouter -> gcpSystem.backendAPI.configurationService "Get user configurations"
        gcpSystem.backendAPI.userRouter -> gcpSystem.backendAPI.portfolioService "Get user portfolios"

        gcpSystem.backendAPI.sustainabilityRouter -> gcpSystem.backendAPI.configurationService "Get configuration"
        gcpSystem.backendAPI.sustainabilityRouter -> gcpSystem.backendAPI.sustainabilityProvider "Calculate impacts"

        gcpSystem.backendAPI.costsRouter -> gcpSystem.backendAPI.costsProviderService "Compute usage costs"

        gcpSystem.backendAPI.cacheService -> cache.cacheSystem "Cache results"
        gcpSystem.backendAPI.cacheService -> cache.cacheSystem.scheduler "Schedule API Calls"

        cache.cacheSystem -> databaseSystem "Store/Retrieve Cached Assets"

        gcpSystem.webDashboard -> gcpSystem.backendAPI.electricityRouter "Makes API calls to" "JSON/HTTPS"

        gcpSystem.webDashboard -> googleIdentityProviderSystem "Requests authentication"
        googleIdentityProviderSystem -> gcpSystem.webDashboard "Authenticates user and gives the authorization code"
        gcpSystem.webDashboard -> gcpSystem.backendAPI.authRouter "Authenticate user using the authorization code"
        gcpSystem.backendAPI.authRouter -> gcpSystem.webDashboard "Generates access-token and sends it"
    }

    views {
        systemContext gcpSystem "Context" "System Context Diagram" {
            include *
            exclude databaseSystem cache fileSystem
            autolayout lr
        }

        container gcpSystem "Container_Diagram" "Container Diagram" {
            include *
            exclude databaseSystem cache fileSystem
            autolayout lr
        }

        component gcpSystem.backendAPI "BackendAPI_Full" "Component Diagram (Full Architecture)" {
            include *
            include databaseSystem
            include cache.cacheSystem
            autolayout tb
        }

        container cache "Cache_Architecture" "The container view of the Cache System" {
            include *
            autolayout lr
        }

        # =========================================================
        # DYNAMIC VIEWS
        # =========================================================
        dynamic gcpSystem.backendAPI "Calculation_Flow" "Electricity Cost Calculation Flow" {
            gcpSystem.webDashboard -> gcpSystem.backendAPI.electricityRouter "Request Cost Analysis"
            gcpSystem.backendAPI.electricityRouter -> gcpSystem.backendAPI.costsProviderService "Calculate Costs"
            gcpSystem.backendAPI.costsProviderService -> cache.cacheSystem "Check Cache"
            gcpSystem.backendAPI.costsProviderService -> electricityMapsSystem "Fetch Live Data (if cache miss)"
            autolayout lr
        }

        dynamic gcpSystem.backendAPI "Authentication_Flow" "Authentication Flow" {
            gcpSystem.webDashboard -> googleIdentityProviderSystem "Requests authentication"
            googleIdentityProviderSystem -> gcpSystem.webDashboard "Authenticates user and gives the authorization code"
            gcpSystem.webDashboard -> gcpSystem.backendAPI.authRouter "Authenticate user using the authorization code"
            gcpSystem.backendAPI.authRouter -> gcpSystem.webDashboard "Generates access-token and sends it"
            autolayout lr

        }

        component cache.cacheSystem "Cache_Internals" "Internals of the Cache Container" {
            include *
            autolayout tb
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
                background #2e6bff
                stroke #ffffff
                color #ffffff
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
                strokeWidth 2
                color #444444
            }
        }
    }
}