USE housing
GO

SELECT * 
FROM housing_info

/*UPDATE seems to be working but there are no visible changes in the data.
SELECT SaleDate, CONVERT(DATE, SaleDate)
FROM housing_info

Checking if the user has a permission to perform UPDATE.
EXEC sp_table_privileges 
   @table_name = 'housing_info' */

/*This query converts datetime type into date type. As a result, it perform the action of removing the unwanted zeros.*/
ALTER TABLE housing_info
ALTER COLUMN SaleDate DATE

/*A longer solution.
SELECT  t1.ParcelID, t1.PropertyAddress, t2.ParcelID, t2.PropertyAddress, ISNULL(t1.PropertyAddress, t2.PropertyAddress)
FROM	housing_info t1
JOIN	housing_info t2
ON		t1.ParcelID = t2.ParcelID
AND		t1.UniqueID != t2.UniqueID
WHERE	t1.PropertyAddress IS NULL */

/* This query is twice as fast. It creates a common table expression which stores a previous property address on the list which always corresponds
to the property coming after that has a NULL value */
WITH CTE AS(
SELECT ParcelID, previous_property
FROM (
	SELECT
		PropertyAddress,
		ParcelID,
		LAG (PropertyAddress) OVER (ORDER BY (ParcelID)) AS previous_property
		--LEAD(PropertyAddress) OVER (ORDER BY (ParcelID)) AS next_property
	FROM housing_info
)  prev_next_prop
WHERE PropertyAddress IS NULL
)

UPDATE housing_info
SET PropertyAddress = CTE.previous_property
FROM housing_info
JOIN CTE ON housing_info.ParcelID = CTE.ParcelID



/*Split the PropertyAddress string in two parts.*/

/*Add a new column for the street and city and fill it with data.*/
ALTER TABLE housing_info
ADD PropertyAddressStreet NVARCHAR(200),
ADD PropertyAddressCity NVARCHAR(20)

UPDATE housing_info
SET PropertyAddressStreet = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)- 1),
SET PropertyAddressCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, LEN(PropertyAddress))



/*Delete the PropertyAddress column.*/
ALTER TABLE	housing_info
DROP COLUMN PropertyAddress 

/*Alter OwnerAddress column. Separate it in three parts.*/
ALTER TABLE housing_info
ADD OwnerAddressStreet NVARCHAR(128),
	OwnerAddressCity NVARCHAR(20),
	OwnerAddressState NVARCHAR(20)

UPDATE housing_info
SET OwnerAddressStreet = PARSENAME(REPLACE(OwnerAddress,',', '.'), 3),
	OwnerAddressCity = PARSENAME(REPLACE(OwnerAddress,',', '.'),2), 
	OwnerAddressState = PARSENAME(REPLACE(OwnerAddress,',', '.'),1)

ALTER TABLE	housing_info
DROP COLUMN OwnerAddress 

/* This query should make the desired change with leaving 'Yes'/'No' as they were. However, UPDATE isn't working.
Not sure why.
UPDATE housing_info
SET SoldAsVacant = REPLACE(SoldAsVacant,'Y ', 'Yes')
--SoldAsVacant = REPLACE(SoldAsVacant,'N  ', 'No') */


/*This query makes the same update using CASE-WHEN*/
UPDATE housing_info
SET SoldAsVacant = 
		CASE
			WHEN SoldAsVacant = 'N' THEN 'No'
			WHEN SoldAsVacant = 'Y' THEN 'Yes'
			ELSE SoldAsVacant
		END
	FROM housing_info

/* This CTE is helpful for checking whether there are duplicates in data. It can be used to delete duplicates as well.
WITH CTE AS  (
	SELECT  ParcelID, LegalReference, SaleDate, 
			COUNT(ParcelID) AS 'c'
	FROM housing_info
	GROUP BY ParcelID, LegalReference, SaleDate
	HAVING COUNT(ParcelID) > 1
) */

/* Alternate way to remove duplicates using a windows function ROW_NUMBER */
DELETE 
FROM housing_info
WHERE UniqueID IN (
	SELECT UniqueID  
	FROM (
		SELECT  UniqueID, 
				ROW_NUMBER() OVER (PARTITION BY ParcelID, LegalReference, SaleDate ORDER BY ParcelID) AS row_num
		FROM housing_info
	) duplicates
	WHERE duplicates.row_num > 1
)



