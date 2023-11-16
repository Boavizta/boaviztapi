package main

import (
	"encoding/csv"
	"errors"
	"fmt"
	"log"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type VantageExport struct {
	Name                          string
	APIName                       string
	InstanceMemory                float64
	ComputeUnitsECU               string
	vCPUs                         float64
	GiBOfMemoryPerVcpu            string
	GPUs                          string
	GPUModel                      string
	GPUMemory                     string
	CUDAComputeCapability         string
	FPGAs                         string
	ECUPerVcpu                    string
	PhysicalProcessor             string
	ClockSpeedGHz                 string
	InstanceStorage               string
	Arch                          string
	NetworkPerformance            string
	EBSOptimizedBaselineBandwidth string
	AvailabilityZones             string
	OnDemandCost                  string
}

type BoaviztaAWSData struct {
	ID                         string
	Manufacturer               string
	CaseType                   string
	Year                       string
	Vcpu                       string
	PlatformVcpu               string
	CPUUnits                   string
	CPUCoreUnits               string
	CPUName                    string
	CPUManufacturer            string
	CPUModelRange              string
	CPUFamily                  string
	CPUTdp                     string
	CPUManufactureDate         string
	InstanceRamCapacity        string
	RAMCapacity                string
	RAMUnits                   string
	SSDUnits                   string
	SSDCapacity                string
	HDDUnits                   string
	HDDCapacity                string
	GPUName                    string
	GPUUnits                   string
	GPUTDP                     string
	GPUMemoryCapacity          string
	PowerSupplyUnits           string
	PowerSupplyUnitWeight      string
	UsageInstancePerServer     string
	UsageTimeWorkload          string
	UsageUseTimeRatio          string
	UsageHoursLifeTime         string
	UsageOtherConsumptionRatio string
	UsageOvercommitted         string
	Warnings                   string
}

func main() {
	vantageExportPath := "vantage-export.csv"
	awsFilePath := "../../boaviztapi/data/archetypes/cloud/aws.csv"
	cpuSpecFilePath := "../../boaviztapi/data/crowdsourcing/cpu_specs.csv"

	vantageExport := loadVantageExport(vantageExportPath)
	existingData := loadExistingData(awsFilePath)
	cpuSpecData := loadCpuSpecData(cpuSpecFilePath)

	var missingInstances []VantageExport

	for _, instance := range vantageExport {
		excluded := false
		for _, exclude := range existingData {
			if instance.APIName == exclude.ID {
				excluded = true
				break
			}
		}
		if !excluded {
			missingInstances = append(missingInstances, instance)
		}
	}

	// Print instances
	for i, instance := range missingInstances {
		fmt.Printf("№ %d adding: %s\n", i, instance.APIName)
	}

	// Append missing instances to existing instances
	var newData []BoaviztaAWSData
	for _, instance := range missingInstances {
		nd := BoaviztaAWSData{
			ID:                         getID(instance),
			Manufacturer:               getManufacturer(instance),
			CaseType:                   getCaseType(instance),
			Year:                       getYear(instance),
			Vcpu:                       getVcpu(instance),
			PlatformVcpu:               getPlatformVcpu(instance, vantageExport),
			CPUUnits:                   getCPUUnits(instance, vantageExport),
			CPUCoreUnits:               getCPUCoreUnits(instance, cpuSpecData),
			CPUName:                    getCPUName(instance),
			CPUManufacturer:            getCPUManufacturer(instance),
			CPUModelRange:              getCPUModelRange(instance),
			CPUFamily:                  getCPUFamily(instance),
			CPUTdp:                     getCPUTdp(instance, cpuSpecData),
			CPUManufactureDate:         getCPUManufactureDate(instance),
			InstanceRamCapacity:        getInstanceRamCapacity(instance),
			RAMCapacity:                getRAMCapacity(instance, vantageExport),
			RAMUnits:                   getRAMUnits(instance, vantageExport),
			SSDUnits:                   getSSDUnits(instance),
			SSDCapacity:                getSSDCapacity(instance),
			HDDUnits:                   getHDDUnits(instance),
			HDDCapacity:                getHDDCapacity(instance),
			GPUName:                    getGPUName(instance),
			GPUUnits:                   getGPUUnits(instance),
			GPUTDP:                     getGPUTDP(instance),
			GPUMemoryCapacity:          getGPUMemoryCapacity(instance),
			PowerSupplyUnits:           getPowerSupplyUnits(instance),
			PowerSupplyUnitWeight:      getPowerSupplyUnitWeight(instance),
			UsageInstancePerServer:     getUsageInstancePerServer(instance, vantageExport),
			UsageTimeWorkload:          getUsageTimeWorkload(instance),
			UsageUseTimeRatio:          getUsageUseTimeRatio(instance),
			UsageHoursLifeTime:         getUsageHoursLifeTime(instance),
			UsageOtherConsumptionRatio: getUsageOtherConsumptionRatio(instance),
			UsageOvercommitted:         getUsageOvercommitted(instance),
			Warnings:                   getWarnings(instance),
		}

		newData = append(newData, nd)
	}

	sort.Slice(newData, func(i, j int) bool {
		return instanceLess(newData[i].ID, newData[j].ID)
	})

	appendToCSV(awsFilePath, newData)
}

func instanceLess(a, b string) bool {
	partsA := strings.Split(a, ".")
	partsB := strings.Split(b, ".")

	// Compare the prefixes (e.g., "c6a")
	if partsA[0] != partsB[0] {
		return partsA[0] < partsB[0]
	}

	// Extract the numbers from the suffixes (e.g., "16" from "16xlarge")
	numA, errA := strconv.Atoi(strings.TrimSuffix(partsA[1], "xlarge"))
	numB, errB := strconv.Atoi(strings.TrimSuffix(partsB[1], "xlarge"))

	// If either string doesn't follow the expected format, fall back to lexicographic comparison
	if errA != nil || errB != nil {
		if partsA[1] == "large" || partsB[1] == "large" {
			res := partsA[1] > partsB[1]
			return res
		}
		return a < b
	}

	return numA < numB
}

func loadVantageExport(fileName string) []VantageExport {
	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Failed to open file:", err)
		return nil
	}
	defer file.Close()

	r := csv.NewReader(file)
	records, err := r.ReadAll()
	if err != nil {
		fmt.Println("Failed to read CSV:", err)
		return nil
	}

	var instances []VantageExport
	for _, record := range records[1:] { // Skip the header
		instanceMemory, err := convertToFloat64(record[2])
		if err != nil {
			log.Fatal(err)
		}
		vCPUs, err := convertToFloat64(record[4])
		if err != nil {
			log.Fatal(err)
		}
		instance := VantageExport{
			Name:                          record[0],
			APIName:                       record[1],
			InstanceMemory:                instanceMemory,
			ComputeUnitsECU:               record[3],
			vCPUs:                         vCPUs,
			GiBOfMemoryPerVcpu:            record[5],
			GPUs:                          record[6],
			GPUModel:                      record[7],
			GPUMemory:                     record[8],
			CUDAComputeCapability:         record[9],
			FPGAs:                         record[10],
			ECUPerVcpu:                    record[11],
			PhysicalProcessor:             record[12],
			ClockSpeedGHz:                 record[13],
			InstanceStorage:               record[18],
			Arch:                          record[21],
			NetworkPerformance:            record[22],
			EBSOptimizedBaselineBandwidth: record[23],
			AvailabilityZones:             record[28],
			OnDemandCost:                  record[29],
		}
		instances = append(instances, instance)
	}

	return instances
}

func loadExistingData(fileName string) []BoaviztaAWSData {
	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Failed to open file:", err)
		return nil
	}
	defer file.Close()

	r := csv.NewReader(file)
	records, err := r.ReadAll()
	if err != nil {
		fmt.Println("Failed to read CSV:", err)
		return nil
	}

	var instances []BoaviztaAWSData
	for _, record := range records[1:] { // Skip the header
		instance := BoaviztaAWSData{
			ID: record[0],
		}
		instances = append(instances, instance)
	}

	return instances
}

type CpuSpecData struct {
	TDP   string
	Cores string
}

func loadCpuSpecData(filePath string) map[string]CpuSpecData {
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Failed to open file:", err)
		return nil
	}
	defer file.Close()

	r := csv.NewReader(file)
	records, err := r.ReadAll()
	if err != nil {
		fmt.Println("Failed to read CSV:", err)
		return nil
	}

	var instances map[string]CpuSpecData = map[string]CpuSpecData{}
	for _, record := range records[1:] { // Skip the header
		instances[record[0]] = CpuSpecData{
			Cores: record[7],
			TDP:   record[6],
		}
	}

	return instances
}

func appendToCSV(fileName string, newData []BoaviztaAWSData) {
	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)

	// Write new data rows
	for _, data := range newData {
		row := []string{
			data.ID,
			data.Manufacturer,
			data.CaseType,
			data.Year,
			data.Vcpu,
			data.PlatformVcpu,
			data.CPUUnits,
			data.CPUCoreUnits,
			data.CPUName,
			data.CPUManufacturer,
			data.CPUModelRange,
			data.CPUFamily,
			data.CPUTdp,
			data.CPUManufactureDate,
			data.InstanceRamCapacity,
			data.RAMCapacity,
			data.RAMUnits,
			data.SSDUnits,
			data.SSDCapacity,
			data.HDDUnits,
			data.HDDCapacity,
			data.GPUName,
			data.GPUUnits,
			data.GPUTDP,
			data.GPUMemoryCapacity,
			data.PowerSupplyUnits,
			data.PowerSupplyUnitWeight,
			data.UsageInstancePerServer,
			data.UsageTimeWorkload,
			data.UsageUseTimeRatio,
			data.UsageHoursLifeTime,
			data.UsageOtherConsumptionRatio,
			data.UsageOvercommitted,
			data.Warnings,
		}
		if err := writer.Write(row); err != nil {
			fmt.Println("Error writing to CSV:", err)
			return
		}
	}

	// Flush the CSV writer to ensure all data gets written to the underlying writer
	writer.Flush()

	if err := writer.Error(); err != nil {
		fmt.Println("Error:", err)
	}
}

func convertToFloat64(s string) (float64, error) {
	// Split the string based on space to get the number and the unit
	parts := strings.Split(s, " ")
	if len(parts) < 2 {
		return 0, fmt.Errorf("invalid format")
	}

	// Convert the number part to float64
	return strconv.ParseFloat(parts[0], 64)
}

func getID(instance VantageExport) string {
	return instance.APIName
}

func getManufacturer(instance VantageExport) string {
	return "AWS"
}

func getCaseType(instance VantageExport) string {
	return "rack"
}

func getYear(instance VantageExport) string {
	return "" // not used in the calculation, so I wouldn't make this data mandatory
}

func getVcpu(instance VantageExport) string {
	return strconv.FormatFloat(instance.vCPUs, 'f', -1, 64)
}

func getMetal(instance VantageExport, allInstances []VantageExport) VantageExport {
	parts := strings.Split(instance.APIName, ".")
	if len(parts) < 2 {
		panic("fuck")
	}

	// Not all instance types have a .metal instance. Therefore we use the largest instancetype as platform in these cases.
	// I just created a list with all instances to make it explicit
	// https://go.dev/play/p/EW2zGveEVSe
	// https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#instance-type-names
	largestInstance := map[string]string{
		"m5":         "metal",
		"m5a":        "24xlarge",
		"m5ad":       "24xlarge",
		"m5d":        "metal",
		"m5dn":       "metal",
		"m5n":        "metal",
		"m5zn":       "metal",
		"m6a":        "metal",
		"m6g":        "metal",
		"m6gd":       "metal",
		"m6i":        "metal",
		"m6id":       "metal",
		"m6idn":      "metal",
		"m6in":       "metal",
		"m7a":        "metal-48xl",
		"m7g":        "metal",
		"m7gd":       "16xlarge",
		"m7i":        "48xlarge",
		"m7i-flex":   "8xlarge",
		"mac1":       "metal",
		"mac2":       "metal",
		"mac2-m2pro": "metal",
		"t2":         "2xlarge",
		"t3":         "2xlarge",
		"t3a":        "2xlarge",
		"t4g":        "2xlarge",
		"c5a":        "24xlarge",
		"c5ad":       "24xlarge",
		"c5d":        "metal",
		"c5n":        "metal",
		"c6a":        "metal",
		"c6g":        "metal",
		"c6gd":       "metal",
		"c6gn":       "16xlarge",
		"c6i":        "metal",
		"c6id":       "metal",
		"c6in":       "metal",
		"c7a":        "metal-48xl",
		"c7g":        "metal",
		"c7gd":       "16xlarge",
		"c7gn":       "16xlarge",
		"c7i":        "48xlarge",
		"hpc6a":      "48xlarge",
		"hpc7g":      "16xlarge",
		"hpc7a":      "96xlarge",
		"r5":         "metal",
		"r5a":        "24xlarge",
		"r5ad":       "24xlarge",
		"r5b":        "metal",
		"r5d":        "metal",
		"r5dn":       "metal",
		"r5n":        "metal",
		"r6a":        "metal",
		"r6g":        "metal",
		"r6gd":       "metal",
		"r6i":        "metal",
		"r6idn":      "metal",
		"r6in":       "metal",
		"r6id":       "metal",
		"r7a":        "metal-48xl",
		"r7g":        "metal",
		"r7gd":       "16xlarge",
		"r7iz":       "32xlarge",
		"u-3tb1":     "56xlarge",
		"u-6tb1":     "metal",
		"u-9tb1":     "metal",
		"u-12tb1":    "metal",
		"u-18tb1":    "metal",
		"u-24tb1":    "metal",
		"x1":         "32xlarge",
		"x2gd":       "metal",
		"x2idn":      "metal",
		"x2iedn":     "metal",
		"x2iezn":     "metal",
		"x1e":        "32xlarge",
		"z1d":        "metal",
		"d3":         "8xlarge",
		"d3en":       "12xlarge",
		"h1":         "16xlarge",
		"i3":         "metal",
		"i3en":       "metal",
		"i4g":        "16xlarge",
		"i4i":        "metal",
		"im4gn":      "16xlarge",
		"is4gen":     "8xlarge",
		"f1":         "16xlarge",
		"g3":         "16xlarge",
		"g4ad":       "16xlarge",
		"g4dn":       "metal",
		"g5":         "48xlarge",
		"g5g":        "metal",
		"inf1":       "24xlarge",
		"inf2":       "48xlarge",
		"p2":         "16xlarge",
		"p3":         "16xlarge",
		"p3dn":       "24xlarge",
		"p4d":        "24xlarge",
		"p4de":       "24xlarge",
		"p5":         "48xlarge",
		"trn1":       "32xlarge",
		"trn1n":      "32xlarge",
		"vt1":        "24xlarge",
		"a1":         "metal",
		"c1":         "xlarge",
		"c3":         "8xlarge",
		"c4":         "8xlarge",
		"g2":         "8xlarge",
		"i2":         "8xlarge",
		"m1":         "xlarge",
		"m2":         "4xlarge",
		"m3":         "2xlarge",
		"m4":         "16xlarge",
		"r3":         "8xlarge",
		"r4":         "16xlarge",
		"t1":         "micro",
	}
	platformString := largestInstance[parts[0]]

	if platformString == "" {
		platformString = "metal" // default
	}

	// If this is platform instance, return itself
	if parts[1] == platformString {
		return instance
	}

	metalString := fmt.Sprintf("%s.%s", parts[0], platformString)

	// find the metal instance
	for _, ve := range allInstances {
		if ve.APIName == metalString {
			return ve
		}
	}

	// in case there is no metal instance we asumme that this instance is platform/metal
	return instance
}

func getPlatformVcpu(instance VantageExport, allInstances []VantageExport) string {
	metalInstance := getMetal(instance, allInstances)

	return strconv.FormatFloat(metalInstance.vCPUs, 'f', -1, 64)
}

func getThreadsPerCpu(cpuName string) (float64, error) {
	var threadsPerCpu float64
	var err error = nil

	threadMap := map[string]float64{
		"Xeon Platinum 8375C":  64,
		"Xeon Platinum 6455B":  32,
		"Xeon Platinum 8176M":  56, // https://en.wikichip.org/wiki/intel/xeon_platinum/8176m
		"Xeon Platinum 8252C":  24, // https://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%208252C.html
		"Xeon Platinum 8259CL": 48, // https://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%208259CL.html
		"Xeon Platinum 8275CL": 48, // https://www.cpu-world.com/CPUs/Xeon/Intel-Xeon%208275CL.html
		"Xeon Platinum 8280L":  56, // https://ark.intel.com/content/www/us/en/ark/products/192472/intel-xeon-platinum-8280l-processor-38-5m-cache-2-70-ghz.html
		"Apple M1 chip with 8-core CPU, 8-core GPU, and 16-core Neural Engine": 8, // Just a guess
		"Xeon E5-2670 v2": 16, // https://www.intel.com/content/www/us/en/products/sku/64595/intel-xeon-processor-e52670-20m-cache-2-60-ghz-8-00-gts-intel-qpi/specifications.html
		"Graviton2":       64, // https://en.wikipedia.org/wiki/AWS_Graviton#Graviton2
		"Graviton3":       64, // https://en.wikipedia.org/wiki/AWS_Graviton#Graviton3
		"EPYC 9R14":       96, // Just a guess
		"EPYC 7R13":       96, // https://gadgetversus.com/processor/amd-epyc-7r13-specs/
		"EPYC 7R32":       96, // https://www.cpubenchmark.net/cpu.php?cpu=AMD+EPYC+7R32&id=3894
	}

	threadsPerCpu, success := threadMap[cpuName]
	if !success {
		return 0, errors.New("cpuName didn't mactch any known thread number")
	}

	return threadsPerCpu, err
}

// CPU in the platform
func getCPUUnits(instance VantageExport, allInstances []VantageExport) string {
	// platform_vcpu / threads_per_cpu
	cpuName := getCPUName(instance)
	if cpuName == "" {
		return ""
	}
	threadsPerCpu, err := getThreadsPerCpu(cpuName)
	if err != nil {
		log.Fatalf("%s: %v", cpuName, err)
		return ""
	}
	platformVCPUstring := getPlatformVcpu(instance, allInstances)
	platformVCPU, err := strconv.ParseFloat(platformVCPUstring, 64)
	if err != nil {
		log.Fatalf("getCPUUnits: %v", err)
	}

	CPUUnits := platformVCPU / threadsPerCpu
	return strconv.FormatFloat(CPUUnits, 'f', -1, 64)
}

func getCPUCoreUnits(instance VantageExport, cpuSpecData map[string]CpuSpecData) string {
	CPUName := getCPUName(instance)
	CPUManufacturer := getCPUManufacturer(instance)
	name := fmt.Sprintf("%s %s", CPUManufacturer, CPUName)
	cpuSpec := cpuSpecData[name]
	CPUCoreUnits := cpuSpec.Cores
	return CPUCoreUnits
}

// returns: name, manufacturer, model_range, family
func getCPUNaming(instance VantageExport) (string, string, string, string) {
	parts := strings.Split(instance.PhysicalProcessor, " ")

	var rgx = regexp.MustCompile(`\((.*?)\)`)
	rs := rgx.FindStringSubmatch(instance.PhysicalProcessor)
	var insideParentheses string
	if len(rs) > 1 {
		insideParentheses = rs[1]
	}

	if instance.PhysicalProcessor == "AWS Graviton2 Processor" {
		return "Graviton2", "Annapurna Labs", "Graviton2", "Graviton2"
	} else if instance.PhysicalProcessor == "AWS Graviton Processor" {
		return "Graviton2", "Annapurna Labs", "Graviton", "Graviton"
	} else if instance.PhysicalProcessor == "AWS Graviton3 Processor" {
		return "Graviton3", "Annapurna Labs", "Graviton3", "Graviton3"
	} else if strings.HasPrefix(instance.PhysicalProcessor, "AMD EPYC") {
		return parts[1] + " " + parts[2], "AMD", "epyc", "naple"
	} else if instance.PhysicalProcessor == "Intel Xeon Family" {
		return "Xeon", "Intel", "xeon", ""
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon Platinum") {
		return parts[1] + " " + parts[2] + " " + parts[3], "Intel", "xeon platinum", insideParentheses
	} else if instance.PhysicalProcessor == "Intel Xeon 8375C (Ice Lake)" {
		return "Xeon Platinum 8375C", "Intel", "xeon platinum", "Ice Lake"
	} else if instance.PhysicalProcessor == "Intel Xeon Scalable (Icelake)" {
		return "Xeon Platinum 8375C", "Intel", "xeon platinum", "Ice Lake"
	} else if instance.PhysicalProcessor == "Intel Xeon Scalable (Sapphire Rapids)" {
		return "", "Intel", "xeon platinum", "Sapphire Rapids"
	} else if instance.PhysicalProcessor == "Intel Xeon Scalable (Skylake)" {
		return "Xeon Platinum 8176M", "Intel", "xeon platinum", "Skylake"
	} else if instance.PhysicalProcessor == "Intel Skylake E5 2686 v5" {
		return "Xeon E5-2686 v5", "Intel", "xeon e5", "Skylake"
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon E5-") {
		parts2 := strings.Split(parts[2], "-")
		return parts[1] + " " + parts[2] + " " + parts[3], "Intel", parts[1] + " " + parts2[0], insideParentheses
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon E") {
		return instance.PhysicalProcessor, "Intel", parts[1] + " " + parts[2], insideParentheses
	} else {
		return instance.PhysicalProcessor, "", "", "" // If nothing else
	}
}

func getCPUName(instance VantageExport) string {
	name, _, _, _ := getCPUNaming(instance)

	// Fix bad info
	if name == "Xeon Platinum 8252" {
		name = "Xeon Platinum 8252C"
	} else if name == "Xeon Platinum 8275L" {
		name = "Xeon Platinum 8275CL"
	}

	return name
}

func getCPUManufacturer(instance VantageExport) string {
	_, manufacturer, _, _ := getCPUNaming(instance)
	return manufacturer
}

func getCPUModelRange(instance VantageExport) string {
	_, _, modelRange, _ := getCPUNaming(instance)
	return modelRange
}

func getCPUFamily(instance VantageExport) string {
	_, _, _, family := getCPUNaming(instance)
	return family
}

func getCPUTdp(instance VantageExport, cpuSpecData map[string]CpuSpecData) string {
	CPUName := getCPUName(instance)
	CPUManufacturer := getCPUManufacturer(instance)
	name := fmt.Sprintf("%s %s", CPUManufacturer, CPUName)
	cpuSpec := cpuSpecData[name]
	TDP := cpuSpec.TDP
	return TDP
}

func getCPUManufactureDate(instance VantageExport) string {
	return "" // not used in the calculation
}

func getInstanceRamCapacity(instance VantageExport) string {
	return strconv.FormatFloat(instance.InstanceMemory, 'f', -1, 64)
}

// returns capacity, units
func getRAM(instance VantageExport, allInstances []VantageExport) (string, string) {
	// InstanceRamCapacity_metal = Units * Capacity
	// Only based on metal RAM

	metalInstance := getMetal(instance, allInstances)
	if metalInstance.InstanceMemory < 32.0 {
		return strconv.FormatFloat(metalInstance.InstanceMemory, 'f', -1, 64), "1"
	}

	capacity := 32.0
	RAMUnits := metalInstance.InstanceMemory / capacity
	return "32", strconv.FormatFloat(RAMUnits, 'f', -1, 64)

}

func getRAMCapacity(instance VantageExport, allInstances []VantageExport) string {
	capacity, _ := getRAM(instance, allInstances)
	return capacity
}

func getRAMUnits(instance VantageExport, allInstances []VantageExport) string {
	_, units := getRAM(instance, allInstances)
	return units
}

// returns capacity, units
func getDisk(instance VantageExport) (string, string) {
	// Examples:
	// 600 GB (2 * 300 GB NVMe SSD)
	// 300 GB NVMe SSD
	re := regexp.MustCompile(`(\d+)\s*\*\s*(\d+)`)
	matches := re.FindStringSubmatch(instance.InstanceStorage)

	if matches == nil {
		// Example here: 300 GB NVMe SSD
		parts := strings.Split(instance.InstanceStorage, " ")
		return parts[0], "1"
	}

	// Example here: 600 GB (2 * 300 GB NVMe SSD)
	// units * capacity
	// return capacity, units
	return matches[2], matches[1]
}

// Required
func getSSDUnits(instance VantageExport) string {
	if !strings.Contains(instance.InstanceStorage, "SSD") {
		return "0"
	}
	_, units := getDisk(instance)
	return units
}

// Required
func getSSDCapacity(instance VantageExport) string {
	if !strings.Contains(instance.InstanceStorage, "SSD") {
		return "0"
	}
	capacity, _ := getDisk(instance)
	return capacity
}

// Required
func getHDDUnits(instance VantageExport) string {
	if !strings.Contains(instance.InstanceStorage, "HDD") {
		return "0"
	}
	_, units := getDisk(instance)
	return units
}

// Required
func getHDDCapacity(instance VantageExport) string {
	if !strings.Contains(instance.InstanceStorage, "HDD") {
		return "0"
	}
	capacity, _ := getDisk(instance)
	return capacity
}

func getGPUName(instance VantageExport) string {
	if instance.GPUModel == "None" {
		return ""
	}
	return instance.GPUModel
}

func getGPUUnits(instance VantageExport) string {
	if instance.GPUModel == "None" {
		return ""
	}
	return instance.GPUs
}

func getGPUTDP(instance VantageExport) string {
	return ""
}

func getGPUMemoryCapacity(instance VantageExport) string {
	if instance.GPUModel == "None" {
		return ""
	}
	// memory per gpu_unit
	totalCapacity, err := convertToFloat64(instance.GPUMemory)
	if err != nil {
		panic("error")
	}

	units, err := strconv.ParseFloat(instance.GPUs, 64)
	if err != nil {
		panic("error")
	}

	GPUMemoryCapacity := totalCapacity / units
	GPUMemoryCapacityString := strconv.FormatFloat(GPUMemoryCapacity, 'f', -1, 64)
	return GPUMemoryCapacityString
}

// Required
func getPowerSupplyUnits(instance VantageExport) string {
	return "2;2;2"
}

// Required
func getPowerSupplyUnitWeight(instance VantageExport) string {
	return "2.99;1;5"
}

func getUsageInstancePerServer(instance VantageExport, allInstances []VantageExport) string {
	// metal.vCPU / "vCPUs"
	platformVCPUstring := getPlatformVcpu(instance, allInstances)

	platformVCPU, err := strconv.ParseFloat(platformVCPUstring, 64)
	if err != nil {
		panic("error")
	}

	usageInstancePerServer := platformVCPU / instance.vCPUs

	result := strconv.FormatFloat(usageInstancePerServer, 'f', -1, 64)
	return result
}

func getUsageTimeWorkload(instance VantageExport) string {
	return "50;0;100"
}

func getUsageUseTimeRatio(instance VantageExport) string {
	return "1"
}

func getUsageHoursLifeTime(instance VantageExport) string {
	return "35040" // 4 years
}

func getUsageOtherConsumptionRatio(instance VantageExport) string {
	return "0.33;0.2;0.6"
}

func getUsageOvercommitted(instance VantageExport) string {
	// boolean
	return "0" // not used currently
}

func getWarnings(instance VantageExport) string {
	return "RAM.capacity not verified"
}
