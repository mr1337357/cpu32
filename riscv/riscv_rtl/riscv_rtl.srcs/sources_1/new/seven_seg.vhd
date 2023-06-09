----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/07/2023 11:23:28 PM
-- Design Name: 
-- Module Name: seven_seg - Behavioral
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

entity seven_seg is
    Port ( clk : in STD_LOGIC;
           data : in STD_LOGIC_VECTOR (15 downto 0);
           seg : out STD_LOGIC_VECTOR (7 downto 0);
           ssel : out STD_LOGIC_VECTOR (3 downto 0));
end seven_seg;

architecture Behavioral of seven_seg is
    signal count : std_logic_vector (12 downto 0) := '0'&x"000";
    signal digit : std_logic_vector (3 downto 0);
begin
    process(clk,count,data)
    begin
        if(rising_edge(clk))
        then
            count <= count + 1;
        end if;
        case count(12 downto 10) is
            when "000"   =>
                ssel <= "1110";
                digit  <= data(3  downto  0);
            when "010"   =>
                ssel <= "1101";
                digit  <= data(7  downto  4);
            when "100"   =>
                ssel <= "1011";
                digit  <= data(11 downto  8);
            when "110"   => 
                ssel <= "0111";
                digit  <= data(15 downto 12);
            when others => 
                ssel <= (others => '1');
                digit <= x"8";
    end case;
    end process;
    seg <= "10000001" when digit = x"0" else
           "11111001" when digit = x"1" else
           "10100100" when digit = x"2" else
           "10110000" when digit = x"3" else
           "10011001" when digit = x"4" else
           "10010010" when digit = x"5" else
           "10000011" when digit = x"6" else
           "11111000" when digit = x"7" else
           "10000000" when digit = x"8" else
           "10011000" when digit = x"9" else
           "10001000" when digit = x"A" else
           "10000011" when digit = x"B" else
           "11000110" when digit = x"C" else
           "10100001" when digit = x"D" else
           "10000110" when digit = x"E" else
           "10001110" when digit = x"F" else
           "01111111";
    
end Behavioral;
