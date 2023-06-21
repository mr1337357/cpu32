----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/20/2023 08:21:27 PM
-- Design Name: 
-- Module Name: pc - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity pc is
    Port ( clk : in STD_LOGIC;
           run : in STD_LOGIC;
           jmp : in STD_LOGIC;
           size : in STD_LOGIC;
           address : out STD_LOGIC_VECTOR(31 downto 0);
           jmp_addr : in STD_LOGIC_VECTOR(31 downto 0));
end pc;

architecture Behavioral of pc is
    signal count : std_logic_vector(31 downto 0) := (others => '0');
    signal count_next : std_logic_vector(31 downto 0) := (others => '0');
    signal sel : std_logic_vector(1 downto 0);
begin
    sel <= jmp & size;
    count_next <= 
        count + 2 when sel = "00" else
        count + 4 when sel = "01" else
        jmp_addr  when sel = "1-" else
        (others => '0');
    process(clk,run,count,count_next)
    begin
        if rising_edge(clk)
        then
            if run = '1'
            then
                count <= count_next;
            end if;
        end if;    
    end process;
    
end Behavioral;
