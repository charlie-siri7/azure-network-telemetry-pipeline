SELECT 
    Records.EventTime,
    Records.MacAddress,
    FlowGroups.RuleName,
    ParsedFlow.UnixTimestamp,
    ParsedFlow.SourceIP,
    ParsedFlow.DestinationIP,
    ParsedFlow.SourcePort,
    ParsedFlow.DestinationPort,
    ParsedFlow.Protocol,
    ParsedFlow.TrafficFlow,
    ParsedFlow.TrafficDecision,
    ParsedFlow.FlowState,
    ParsedFlow.PacketsSrcToDest,
    ParsedFlow.BytesSrcToDest,
    ParsedFlow.PacketsDestToSrc,
    ParsedFlow.BytesDestToSrc
FROM 
    OPENROWSET(
        BULK 'URL/y=*/m=*/d=*/h=*/m=*/macAddress=*/PT1H.json',
        FORMAT = 'CSV',
        FIELDQUOTE = '0x0b',
        FIELDTERMINATOR ='0x0b',
        ROWTERMINATOR = '0x0b'
    ) WITH (
        jsonDoc varchar(max)
    ) AS rowset
    CROSS APPLY OPENJSON(jsonDoc, '$.records') WITH (
        EventTime datetime2 '$.time',
        MacAddress varchar(100) '$.macAddress',
        flowRecords nvarchar(max) '$.flowRecords' AS JSON
    ) AS Records
    CROSS APPLY OPENJSON(Records.flowRecords, '$.flows') WITH (
        aclID varchar(100) '$.aclID',
        flowGroups nvarchar(max) '$.flowGroups' AS JSON
    ) AS Flows
    CROSS APPLY OPENJSON(Flows.flowGroups) WITH (
        RuleName varchar(100) '$.rule',
        flowTuples nvarchar(max) '$.flowTuples' AS JSON
    ) AS FlowGroups
    CROSS APPLY OPENJSON(FlowGroups.flowTuples) AS FlowTuples
    
    -- Wrap the array in {} so SQL evaluates it as a single object
    CROSS APPLY OPENJSON('{"row": ["' + REPLACE(FlowTuples.value, ',', '","') + '"]}') WITH (
        UnixTimestamp varchar(50) '$.row[0]',
        SourceIP varchar(50) '$.row[1]',
        DestinationIP varchar(50) '$.row[2]',
        SourcePort varchar(10) '$.row[3]',
        DestinationPort varchar(10) '$.row[4]',
        Protocol varchar(10) '$.row[5]',
        TrafficFlow varchar(5) '$.row[6]', 
        TrafficDecision varchar(5) '$.row[7]',
        FlowState varchar(5) '$.row[8]',
        PacketsSrcToDest varchar(50) '$.row[9]',
        BytesSrcToDest varchar(50) '$.row[10]',
        PacketsDestToSrc varchar(50) '$.row[11]',
        BytesDestToSrc varchar(50) '$.row[12]'
    ) AS ParsedFlow;