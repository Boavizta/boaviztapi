package main

import (
	"encoding/csv"
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

	vantageExport := loadVantageExport(vantageExportPath)
	existingData := loadExistingData(awsFilePath)

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
			CPUUnits:                   getCPUUnits(instance),
			CPUCoreUnits:               getCPUCoreUnits(instance),
			CPUName:                    getCPUName(instance),
			CPUManufacturer:            getCPUManufacturer(instance),
			CPUModelRange:              getCPUModelRange(instance),
			CPUFamily:                  getCPUFamily(instance),
			CPUTdp:                     getCPUTdp(instance),
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

// CPU in the platform
func getCPUUnits(instance VantageExport) string {
	// platform_vcpu / nb_vcpu(cpu_name)
	return "" // TODO @JacobValdemar: Actually attempt to get this value
}

func getCPUCoreUnits(instance VantageExport) string {
	return ""
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
		return parts[1] + " " + parts[2], "amd", "epyc", "naple"
	} else if instance.PhysicalProcessor == "Intel Xeon Family" {
		return "Xeon", "intel", "xeon", ""
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon E") {
		return instance.PhysicalProcessor, "intel", parts[1] + " " + parts[2], insideParentheses
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon Platinum") {
		return parts[1] + " " + parts[2] + " " + parts[3], "intel", "xeon platinum", insideParentheses
	} else if instance.PhysicalProcessor == "Intel Xeon 8375C (Ice Lake)" {
		return "Xeon Platinum 8375C", "intel", "xeon platinum", "Ice Lake"
	} else if strings.HasPrefix(instance.PhysicalProcessor, "Intel Xeon Scalable") {
		return "Xeon", "intel", "xeon scalable", insideParentheses
	} else if instance.PhysicalProcessor == "Intel Skylake E5 2686 v5" {
		return "Skylake E5 2686 v5", "intel", "xeon scalable", "Skylake"
	} else {
		return instance.PhysicalProcessor, "", "", "" // If nothing else
	}
}

func getCPUName(instance VantageExport) string {
	name, _, _, _ := getCPUNaming(instance)
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

func getCPUTdp(instance VantageExport) string {
	return ""
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
